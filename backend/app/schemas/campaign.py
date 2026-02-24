from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    campaign_type: str  # one_to_one, one_to_many
    channel: str = "linkedin_message"
    target_segment: Optional[str] = None
    segment_filters: dict = {}
    sap_solution_focus: list = []
    value_proposition: Optional[str] = None
    message_framework: dict = {}
    sequence_steps: list = []
    tags: list = []


class CampaignCreate(CampaignBase):
    stakeholder_ids: list[int] = []


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    channel: Optional[str] = None
    target_segment: Optional[str] = None
    segment_filters: Optional[dict] = None
    sap_solution_focus: Optional[list] = None
    value_proposition: Optional[str] = None
    message_framework: Optional[dict] = None
    sequence_steps: Optional[list] = None
    status: Optional[str] = None
    tags: Optional[list] = None


class CampaignResponse(CampaignBase):
    id: int
    status: str
    total_contacts: int
    messages_sent: int
    messages_opened: int
    replies_received: int
    meetings_booked: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
