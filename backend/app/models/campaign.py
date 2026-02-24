from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OutreachCampaign(Base):
    __tablename__ = "outreach_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Type
    campaign_type = Column(String(50), nullable=False)  # one_to_one, one_to_many
    channel = Column(
        String(50), default="linkedin_message"
    )  # linkedin_message, linkedin_inmail, email, multi_channel

    # Targeting
    target_segment = Column(Text, nullable=True)  # description of target audience
    segment_filters = Column(JSON, default=dict)  # structured filters
    sap_solution_focus = Column(JSON, default=list)  # which SAP products to pitch

    # Messaging
    value_proposition = Column(Text, nullable=True)
    message_framework = Column(
        JSON, default=dict
    )  # {hook, relevance, value, proof, ask}
    sequence_steps = Column(
        JSON, default=list
    )  # [{step: 1, delay_days: 0, type: "connect"}, ...]

    # Status
    status = Column(String(50), default="draft")  # draft, active, paused, completed

    # Metrics
    total_contacts = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    messages_opened = Column(Integer, default=0)
    replies_received = Column(Integer, default=0)
    meetings_booked = Column(Integer, default=0)

    # Metadata
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("OutreachMessage", back_populates="campaign", lazy="dynamic")
    stakeholders = relationship(
        "CampaignStakeholder", back_populates="campaign", lazy="dynamic"
    )


class CampaignStakeholder(Base):
    __tablename__ = "campaign_stakeholders"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("outreach_campaigns.id"), nullable=False)
    stakeholder_id = Column(Integer, ForeignKey("stakeholders.id"), nullable=False)
    status = Column(
        String(50), default="pending"
    )  # pending, contacted, replied, meeting_booked, not_interested
    current_step = Column(Integer, default=0)
    added_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("OutreachCampaign", back_populates="stakeholders")
    stakeholder = relationship("Stakeholder", backref="campaign_memberships")
