from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CompanyBase(BaseModel):
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[str] = None
    revenue_range: Optional[str] = None
    headquarters_location: Optional[str] = None
    regions: list = []
    current_erp: Optional[str] = None
    current_sap_products: list = []
    sap_maturity_level: str = "unknown"
    digital_transformation_stage: Optional[str] = None
    known_pain_points: list = []
    competitors: list = []
    priority_tier: int = 3
    tags: list = []
    notes: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    employee_count: Optional[str] = None
    revenue_range: Optional[str] = None
    headquarters_location: Optional[str] = None
    regions: Optional[list] = None
    current_erp: Optional[str] = None
    current_sap_products: Optional[list] = None
    sap_maturity_level: Optional[str] = None
    digital_transformation_stage: Optional[str] = None
    known_pain_points: Optional[list] = None
    competitors: Optional[list] = None
    priority_tier: Optional[int] = None
    tags: Optional[list] = None
    notes: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    recent_news: list = []
    ai_company_analysis: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
