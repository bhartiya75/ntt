"""Presentations API — Generate and download PowerPoint presentations."""

import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.models.campaign import OutreachCampaign
from app.schemas.presentation import GeneratePresentationRequest, PresentationResponse
from app.services.ppt_generator import ppt_generator, OUTPUT_DIR
from app.services.toyota_ai_ppt_generator import toyota_ai_generator

router = APIRouter(prefix="/presentations", tags=["presentations"])

VALID_TYPES = ["stakeholder_briefing", "company_analysis", "campaign_summary", "outreach_strategy", "toyota_ai_use_cases"]


@router.post("/generate", response_model=PresentationResponse)
async def generate_presentation(
    request: GeneratePresentationRequest,
    db: Session = Depends(get_db),
):
    """Generate a PowerPoint presentation from sales data."""
    if request.type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid type. Must be one of: {VALID_TYPES}")

    if request.type == "stakeholder_briefing":
        if not request.id:
            raise HTTPException(status_code=400, detail="Stakeholder ID required")
        stakeholder = db.query(Stakeholder).filter(Stakeholder.id == request.id).first()
        if not stakeholder:
            raise HTTPException(status_code=404, detail="Stakeholder not found")
        company = db.query(Company).filter(Company.id == stakeholder.company_id).first() if stakeholder.company_id else None
        result = await ppt_generator.generate_stakeholder_briefing(stakeholder, company, db, request.title, request.ai_provider or "ollama")

    elif request.type == "company_analysis":
        if not request.id:
            raise HTTPException(status_code=400, detail="Company ID required")
        company = db.query(Company).filter(Company.id == request.id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        result = await ppt_generator.generate_company_analysis(company, db, request.title, request.ai_provider or "ollama")

    elif request.type == "campaign_summary":
        if not request.id:
            raise HTTPException(status_code=400, detail="Campaign ID required")
        campaign = db.query(OutreachCampaign).filter(OutreachCampaign.id == request.id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        result = await ppt_generator.generate_campaign_summary(campaign, db, request.title, request.ai_provider or "ollama")

    elif request.type == "outreach_strategy":
        result = await ppt_generator.generate_outreach_strategy(db, request.title, request.ai_provider or "ollama")

    elif request.type == "toyota_ai_use_cases":
        result = await toyota_ai_generator.generate()

    return PresentationResponse(**{k: result[k] for k in ["filename", "download_url", "slides_count", "type"]})


@router.get("/download/{filename}")
async def download_presentation(filename: str):
    """Download a generated PPTX file."""
    safe = os.path.basename(filename)
    path = os.path.join(OUTPUT_DIR, safe)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=safe)


@router.get("/list")
async def list_presentations():
    """List all generated presentations."""
    if not os.path.exists(OUTPUT_DIR):
        return {"presentations": []}
    files = []
    for f in sorted(os.listdir(OUTPUT_DIR), reverse=True):
        if f.endswith(".pptx"):
            fp = os.path.join(OUTPUT_DIR, f)
            files.append({"filename": f, "download_url": f"/api/presentations/download/{f}", "size_bytes": os.path.getsize(fp)})
    return {"presentations": files}
