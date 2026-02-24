"""Outreach API — Generate and manage outreach messages."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.models.outreach_message import OutreachMessage
from app.models.campaign import OutreachCampaign, CampaignStakeholder
from app.schemas.outreach import (
    OutreachMessageResponse,
    GenerateOutreachRequest,
    BulkGenerateRequest,
)
from app.services.outreach_generator import outreach_generator

router = APIRouter(prefix="/outreach", tags=["outreach"])


@router.post("/generate")
async def generate_outreach_messages(
    request: GenerateOutreachRequest,
    db: Session = Depends(get_db),
):
    """Generate personalized outreach messages for one or more stakeholders (1-to-1)."""
    results = []

    for stakeholder_id in request.stakeholder_ids:
        stakeholder = (
            db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
        )
        if not stakeholder:
            results.append({"stakeholder_id": stakeholder_id, "error": "Not found"})
            continue

        company = None
        if stakeholder.company_id:
            company = db.query(Company).filter(Company.id == stakeholder.company_id).first()

        # Generate primary message
        message_data = await outreach_generator.generate_message(
            stakeholder=stakeholder,
            company=company,
            message_type=request.message_type,
            channel=request.channel,
            tone=request.tone,
            sap_solutions=request.sap_solutions or None,
            custom_context=request.custom_context,
            provider=request.ai_provider,
        )

        # Save to database
        message = OutreachMessage(
            campaign_id=request.campaign_id,
            stakeholder_id=stakeholder_id,
            channel=request.channel,
            subject=message_data.get("subject"),
            body=message_data.get("body", ""),
            personalization_context=message_data.get("personalization_context"),
            sap_solutions_referenced=message_data.get("sap_solutions_referenced", []),
            ai_model_used=request.ai_provider,
            variant="A",
        )
        db.add(message)
        db.flush()

        result = {
            "stakeholder_id": stakeholder_id,
            "stakeholder_name": stakeholder.full_name,
            "message_id": message.id,
            "message": message_data,
        }

        # Generate A/B variant if requested
        if request.generate_variants:
            variant_data = await outreach_generator.generate_variant(
                stakeholder=stakeholder,
                company=company,
                original_message=message_data,
                provider=request.ai_provider,
            )
            variant_msg = OutreachMessage(
                campaign_id=request.campaign_id,
                stakeholder_id=stakeholder_id,
                channel=request.channel,
                subject=variant_data.get("subject"),
                body=variant_data.get("body", ""),
                personalization_context=variant_data.get("personalization_context"),
                sap_solutions_referenced=variant_data.get("sap_solutions_referenced", []),
                ai_model_used=request.ai_provider,
                variant="B",
            )
            db.add(variant_msg)
            db.flush()
            result["variant_b"] = {
                "message_id": variant_msg.id,
                "message": variant_data,
            }

        results.append(result)

    db.commit()
    return {"generated": len(results), "results": results}


@router.post("/generate-bulk")
async def generate_bulk_outreach(
    request: BulkGenerateRequest,
    db: Session = Depends(get_db),
):
    """Generate outreach messages for all stakeholders in a campaign (1-to-many)."""
    campaign = (
        db.query(OutreachCampaign)
        .filter(OutreachCampaign.id == request.campaign_id)
        .first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Get all stakeholders in this campaign
    campaign_stakeholders = (
        db.query(CampaignStakeholder)
        .filter(CampaignStakeholder.campaign_id == request.campaign_id)
        .all()
    )

    stakeholder_ids = [cs.stakeholder_id for cs in campaign_stakeholders]

    # Generate using the standard endpoint logic
    gen_request = GenerateOutreachRequest(
        stakeholder_ids=stakeholder_ids,
        campaign_id=request.campaign_id,
        channel=campaign.channel,
        ai_provider=request.ai_provider,
        tone=request.tone,
        message_type=request.message_type,
        sap_solutions=campaign.sap_solution_focus or [],
        custom_context=request.custom_context,
        generate_variants=request.generate_variants,
    )

    return await generate_outreach_messages(gen_request, db)


@router.get("/messages", response_model=list[OutreachMessageResponse])
def list_messages(
    campaign_id: Optional[int] = None,
    stakeholder_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """List outreach messages with filtering."""
    query = db.query(OutreachMessage)
    if campaign_id:
        query = query.filter(OutreachMessage.campaign_id == campaign_id)
    if stakeholder_id:
        query = query.filter(OutreachMessage.stakeholder_id == stakeholder_id)
    if status:
        query = query.filter(OutreachMessage.status == status)
    return query.order_by(OutreachMessage.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/messages/{message_id}", response_model=OutreachMessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Get a single message."""
    message = db.query(OutreachMessage).filter(OutreachMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.patch("/messages/{message_id}/status")
def update_message_status(
    message_id: int, status: str, db: Session = Depends(get_db)
):
    """Update message status (approve, mark as sent, etc.)."""
    message = db.query(OutreachMessage).filter(OutreachMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    valid_statuses = ["draft", "approved", "sent", "replied", "bounced"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}"
        )

    message.status = status
    db.commit()
    return {"message_id": message_id, "status": status}
