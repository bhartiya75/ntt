from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StakeholderBase(BaseModel):
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    linkedin_headline: Optional[str] = None
    linkedin_summary: Optional[str] = None
    linkedin_connections: Optional[int] = None
    linkedin_location: Optional[str] = None
    job_title: Optional[str] = None
    seniority_level: Optional[str] = None
    department: Optional[str] = None
    years_in_role: Optional[int] = None
    career_history: list = []
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    decision_maker_type: Optional[str] = None
    budget_authority: Optional[str] = None
    buying_stage: Optional[str] = None
    pain_points: list = []
    interests: list = []
    content_topics: list = []
    current_sap_experience: Optional[str] = None
    recommended_sap_solutions: list = []
    best_outreach_channel: Optional[str] = None
    engagement_score: float = 0.0
    fit_score: float = 0.0
    tags: list = []
    notes: Optional[str] = None
    source: Optional[str] = None


class StakeholderCreate(StakeholderBase):
    pass


class StakeholderUpdate(BaseModel):
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    linkedin_headline: Optional[str] = None
    linkedin_summary: Optional[str] = None
    job_title: Optional[str] = None
    seniority_level: Optional[str] = None
    department: Optional[str] = None
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    decision_maker_type: Optional[str] = None
    budget_authority: Optional[str] = None
    buying_stage: Optional[str] = None
    pain_points: Optional[list] = None
    interests: Optional[list] = None
    current_sap_experience: Optional[str] = None
    engagement_score: Optional[float] = None
    fit_score: Optional[float] = None
    tags: Optional[list] = None
    notes: Optional[str] = None


class StakeholderResponse(StakeholderBase):
    id: int
    ai_profile_summary: Optional[str] = None
    ai_need_analysis: Optional[str] = None
    ai_gap_analysis: Optional[str] = None
    conversation_starters: list = []
    priority_rank: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StakeholderProfileRequest(BaseModel):
    """Request to run AI profiling on a stakeholder."""
    ai_provider: str = "ollama"  # ollama, claude, or openai
    include_need_analysis: bool = True
    include_gap_analysis: bool = True
    include_conversation_starters: bool = True
    include_solution_matching: bool = True
