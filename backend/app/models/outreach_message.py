from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("outreach_campaigns.id"), nullable=True)
    stakeholder_id = Column(Integer, ForeignKey("stakeholders.id"), nullable=False)

    # Message
    channel = Column(String(50), nullable=False)  # linkedin_message, linkedin_inmail, email
    sequence_step_number = Column(Integer, default=1)
    subject = Column(String(500), nullable=True)  # for email
    body = Column(Text, nullable=False)

    # Personalization
    personalization_context = Column(Text, nullable=True)  # what AI used to personalize
    sap_solutions_referenced = Column(JSON, default=list)
    variant = Column(String(10), nullable=True)  # A, B for A/B testing

    # AI
    ai_model_used = Column(String(50), nullable=True)  # claude, openai
    ai_prompt_used = Column(Text, nullable=True)

    # Status
    status = Column(
        String(50), default="draft"
    )  # draft, approved, sent, replied, bounced
    sent_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("OutreachCampaign", back_populates="messages")
    stakeholder = relationship("Stakeholder", backref="outreach_messages")
