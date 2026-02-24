"""Campaigns API — Create and manage outreach campaigns."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.campaign import OutreachCampaign, CampaignStakeholder
from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.models.outreach_message import OutreachMessage
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.services.segmentation import segmentation_service

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/", response_model=list[CampaignResponse])
def list_campaigns(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    campaign_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all campaigns."""
    query = db.query(OutreachCampaign)
    if status:
        query = query.filter(OutreachCampaign.status == status)
    if campaign_type:
        query = query.filter(OutreachCampaign.campaign_type == campaign_type)
    return query.order_by(OutreachCampaign.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a single campaign."""
    campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/", response_model=CampaignResponse)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db)):
    """Create a new outreach campaign."""
    campaign_data = data.model_dump(exclude={"stakeholder_ids"})
    campaign = OutreachCampaign(**campaign_data)
    db.add(campaign)
    db.flush()

    # Add stakeholders to campaign
    for sid in data.stakeholder_ids:
        stakeholder = db.query(Stakeholder).filter(Stakeholder.id == sid).first()
        if stakeholder:
            cs = CampaignStakeholder(
                campaign_id=campaign.id, stakeholder_id=sid
            )
            db.add(cs)

    campaign.total_contacts = len(data.stakeholder_ids)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: int, data: CampaignUpdate, db: Session = Depends(get_db)):
    """Update a campaign."""
    campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.post("/{campaign_id}/add-stakeholders")
def add_stakeholders_to_campaign(
    campaign_id: int,
    stakeholder_ids: list[int],
    db: Session = Depends(get_db),
):
    """Add stakeholders to an existing campaign."""
    campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    added = 0
    for sid in stakeholder_ids:
        existing = (
            db.query(CampaignStakeholder)
            .filter(
                CampaignStakeholder.campaign_id == campaign_id,
                CampaignStakeholder.stakeholder_id == sid,
            )
            .first()
        )
        if not existing:
            cs = CampaignStakeholder(campaign_id=campaign_id, stakeholder_id=sid)
            db.add(cs)
            added += 1

    campaign.total_contacts += added
    db.commit()
    return {"added": added, "total_contacts": campaign.total_contacts}


@router.post("/{campaign_id}/add-segment")
def add_segment_to_campaign(
    campaign_id: int,
    filters: dict,
    db: Session = Depends(get_db),
):
    """Add a segment of stakeholders to a campaign based on filters."""
    campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    stakeholders = segmentation_service.segment_stakeholders(db, filters)

    added = 0
    for s in stakeholders:
        existing = (
            db.query(CampaignStakeholder)
            .filter(
                CampaignStakeholder.campaign_id == campaign_id,
                CampaignStakeholder.stakeholder_id == s.id,
            )
            .first()
        )
        if not existing:
            cs = CampaignStakeholder(campaign_id=campaign_id, stakeholder_id=s.id)
            db.add(cs)
            added += 1

    campaign.total_contacts += added
    campaign.segment_filters = filters
    db.commit()

    summary = segmentation_service.get_segment_summary(stakeholders)
    return {"added": added, "segment_summary": summary}


@router.get("/{campaign_id}/stakeholders")
def get_campaign_stakeholders(campaign_id: int, db: Session = Depends(get_db)):
    """Get all stakeholders in a campaign."""
    campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign_stakeholders = (
        db.query(CampaignStakeholder)
        .filter(CampaignStakeholder.campaign_id == campaign_id)
        .all()
    )

    result = []
    for cs in campaign_stakeholders:
        stakeholder = (
            db.query(Stakeholder).filter(Stakeholder.id == cs.stakeholder_id).first()
        )
        if stakeholder:
            result.append({
                "stakeholder_id": stakeholder.id,
                "full_name": stakeholder.full_name,
                "job_title": stakeholder.job_title,
                "company_name": stakeholder.company_name,
                "status": cs.status,
                "current_step": cs.current_step,
                "fit_score": stakeholder.fit_score,
                "engagement_score": stakeholder.engagement_score,
            })

    return result
