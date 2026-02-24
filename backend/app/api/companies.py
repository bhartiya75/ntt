"""Companies API — CRUD and analysis endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.services.ai_engine import ai_engine

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/", response_model=list[CompanyResponse])
def list_companies(
    skip: int = 0,
    limit: int = 50,
    search: Optional[str] = None,
    industry: Optional[str] = None,
    sap_maturity_level: Optional[str] = None,
    priority_tier: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List companies with filtering."""
    query = db.query(Company)

    if search:
        query = query.filter(
            Company.name.ilike(f"%{search}%") | Company.industry.ilike(f"%{search}%")
        )
    if industry:
        query = query.filter(Company.industry == industry)
    if sap_maturity_level:
        query = query.filter(Company.sap_maturity_level == sap_maturity_level)
    if priority_tier:
        query = query.filter(Company.priority_tier == priority_tier)

    return query.order_by(Company.priority_tier.asc()).offset(skip).limit(limit).all()


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get a single company by ID."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyResponse)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company."""
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):
    """Update a company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"detail": "Company deleted"}


@router.post("/{company_id}/analyze")
async def analyze_company(
    company_id: int, provider: str = "claude", db: Session = Depends(get_db)
):
    """Run AI analysis on a company — SAP landscape assessment."""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    prompt = f"""Analyze this company for SAP sales opportunities:

Company: {company.name}
Industry: {company.industry or 'Unknown'}
Sub-Industry: {company.sub_industry or 'Unknown'}
Employees: {company.employee_count or 'Unknown'}
Revenue: {company.revenue_range or 'Unknown'}
HQ: {company.headquarters_location or 'Unknown'}
Current ERP: {company.current_erp or 'Unknown'}
Current SAP Products: {', '.join(company.current_sap_products) if company.current_sap_products else 'Unknown'}
SAP Maturity: {company.sap_maturity_level or 'Unknown'}

Provide:
1. Assessment of their likely technology landscape and challenges
2. SAP opportunities (what SAP solutions would benefit them most)
3. Key pain points for their industry
4. Recommended approach for engaging this account
5. Potential deal size and timeline expectations

Write 4-5 detailed paragraphs."""

    analysis = await ai_engine.generate(
        prompt,
        system_prompt="You are a senior SAP sales strategist analyzing target accounts.",
        provider=provider,
    )

    company.ai_company_analysis = analysis
    db.commit()

    return {"company_id": company_id, "analysis": analysis}
