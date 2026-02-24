"""Stakeholders API — CRUD and AI profiling endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.schemas.stakeholder import (
    StakeholderCreate,
    StakeholderUpdate,
    StakeholderResponse,
    StakeholderProfileRequest,
)
from app.services.profiling import profiling_service
from app.services.enrichment import enrichment_service

router = APIRouter(prefix="/stakeholders", tags=["stakeholders"])


@router.get("/", response_model=list[StakeholderResponse])
def list_stakeholders(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    seniority_level: Optional[str] = None,
    department: Optional[str] = None,
    company_id: Optional[int] = None,
    min_fit_score: Optional[float] = None,
    tag: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
):
    """List stakeholders with filtering and sorting."""
    query = db.query(Stakeholder)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Stakeholder.full_name.ilike(search_term)
            | Stakeholder.job_title.ilike(search_term)
            | Stakeholder.company_name.ilike(search_term)
            | Stakeholder.linkedin_headline.ilike(search_term)
        )

    if seniority_level:
        query = query.filter(Stakeholder.seniority_level == seniority_level)
    if department:
        query = query.filter(Stakeholder.department == department)
    if company_id:
        query = query.filter(Stakeholder.company_id == company_id)
    if min_fit_score:
        query = query.filter(Stakeholder.fit_score >= min_fit_score)

    # Sorting
    sort_column = getattr(Stakeholder, sort_by, Stakeholder.created_at)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(skip).limit(limit).all()


@router.get("/{stakeholder_id}", response_model=StakeholderResponse)
def get_stakeholder(stakeholder_id: int, db: Session = Depends(get_db)):
    """Get a single stakeholder by ID."""
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder not found")
    return stakeholder


@router.post("/", response_model=StakeholderResponse)
def create_stakeholder(data: StakeholderCreate, db: Session = Depends(get_db)):
    """Create a new stakeholder."""
    stakeholder = Stakeholder(**data.model_dump())
    db.add(stakeholder)
    db.commit()
    db.refresh(stakeholder)
    return stakeholder


@router.patch("/{stakeholder_id}", response_model=StakeholderResponse)
def update_stakeholder(
    stakeholder_id: int, data: StakeholderUpdate, db: Session = Depends(get_db)
):
    """Update a stakeholder."""
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stakeholder, field, value)

    db.commit()
    db.refresh(stakeholder)
    return stakeholder


@router.delete("/{stakeholder_id}")
def delete_stakeholder(stakeholder_id: int, db: Session = Depends(get_db)):
    """Delete a stakeholder."""
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder not found")
    db.delete(stakeholder)
    db.commit()
    return {"detail": "Stakeholder deleted"}


@router.post("/{stakeholder_id}/profile")
async def generate_profile(
    stakeholder_id: int,
    request: StakeholderProfileRequest,
    db: Session = Depends(get_db),
):
    """Run AI profiling on a stakeholder — generates comprehensive analysis."""
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    company = None
    if stakeholder.company_id:
        company = db.query(Company).filter(Company.id == stakeholder.company_id).first()

    # Generate full AI profile
    profile = await profiling_service.generate_full_profile(
        stakeholder, company, provider=request.ai_provider
    )

    # Update stakeholder with AI analysis
    stakeholder.ai_profile_summary = profile.get("profile_summary")
    stakeholder.ai_need_analysis = profile.get("need_analysis")
    stakeholder.ai_gap_analysis = profile.get("gap_analysis")
    stakeholder.pain_points = profile.get("pain_points", [])
    stakeholder.recommended_sap_solutions = profile.get("recommended_sap_solutions", [])
    stakeholder.conversation_starters = profile.get("conversation_starters", [])
    stakeholder.best_outreach_channel = profile.get("best_outreach_channel")
    stakeholder.engagement_score = profile.get("engagement_score", 0)
    stakeholder.fit_score = profile.get("fit_score", 0)

    db.commit()
    db.refresh(stakeholder)

    return {
        "stakeholder_id": stakeholder_id,
        "profile": profile,
        "status": "Profile generated successfully",
    }


@router.post("/{stakeholder_id}/enrich")
async def enrich_stakeholder(stakeholder_id: int, db: Session = Depends(get_db)):
    """Enrich stakeholder data using Apollo.io."""
    stakeholder = db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    if not stakeholder:
        raise HTTPException(status_code=404, detail="Stakeholder not found")

    result = await enrichment_service.enrich_from_apollo(
        email=stakeholder.email, linkedin_url=stakeholder.linkedin_url
    )

    if not result:
        raise HTTPException(status_code=404, detail="No enrichment data found")

    # Map and update stakeholder
    mapped = enrichment_service.map_apollo_to_stakeholder(result)
    for field, value in mapped.items():
        if value and not getattr(stakeholder, field, None):
            setattr(stakeholder, field, value)

    # Update or create company
    company_mapped = enrichment_service.map_apollo_to_company(result)
    if company_mapped.get("name"):
        existing_company = (
            db.query(Company).filter(Company.name == company_mapped["name"]).first()
        )
        if existing_company:
            for field, value in company_mapped.items():
                if value and not getattr(existing_company, field, None):
                    setattr(existing_company, field, value)
            stakeholder.company_id = existing_company.id
        else:
            new_company = Company(**company_mapped)
            db.add(new_company)
            db.flush()
            stakeholder.company_id = new_company.id

    db.commit()
    db.refresh(stakeholder)

    return {"stakeholder_id": stakeholder_id, "enriched_fields": list(mapped.keys())}
