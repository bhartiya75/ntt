"""Pydantic schemas for Presentation generation."""

from pydantic import BaseModel
from typing import Optional


class GeneratePresentationRequest(BaseModel):
    type: str  # stakeholder_briefing, company_analysis, campaign_summary, outreach_strategy
    id: Optional[int] = None
    title: Optional[str] = None
    ai_provider: Optional[str] = "ollama"


class PresentationResponse(BaseModel):
    filename: str
    download_url: str
    slides_count: int
    type: str
