from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OutreachMessageBase(BaseModel):
    campaign_id: Optional[int] = None
    stakeholder_id: int
    channel: str = "linkedin_message"
    sequence_step_number: int = 1
    subject: Optional[str] = None
    body: str
    variant: Optional[str] = None


class OutreachMessageCreate(OutreachMessageBase):
    pass


class OutreachMessageResponse(OutreachMessageBase):
    id: int
    personalization_context: Optional[str] = None
    sap_solutions_referenced: list = []
    ai_model_used: Optional[str] = None
    status: str
    sent_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class GenerateOutreachRequest(BaseModel):
    """Request to generate AI-powered outreach messages."""
    stakeholder_ids: list[int]
    campaign_id: Optional[int] = None
    channel: str = "linkedin_message"
    ai_provider: str = "ollama"  # claude or openai
    tone: str = "professional"  # professional, casual, thought_leader
    message_type: str = "initial_connect"  # initial_connect, follow_up, value_share, meeting_request
    sap_solutions: list[str] = []  # specific SAP solutions to reference
    custom_context: Optional[str] = None  # additional context for AI
    generate_variants: bool = False  # A/B testing


class BulkGenerateRequest(BaseModel):
    """Request to generate outreach for a segment (1-to-many)."""
    campaign_id: int
    ai_provider: str = "ollama"
    tone: str = "professional"
    message_type: str = "initial_connect"
    custom_context: Optional[str] = None
    generate_variants: bool = False
