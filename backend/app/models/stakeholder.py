from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Stakeholder(Base):
    __tablename__ = "stakeholders"

    id = Column(Integer, primary_key=True, index=True)

    # Identity
    full_name = Column(String(255), nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    # LinkedIn
    linkedin_url = Column(String(500), nullable=True)
    linkedin_headline = Column(String(500), nullable=True)
    linkedin_summary = Column(Text, nullable=True)
    linkedin_connections = Column(Integer, nullable=True)
    linkedin_location = Column(String(255), nullable=True)

    # Professional
    job_title = Column(String(255), nullable=True)
    seniority_level = Column(
        String(50), nullable=True
    )  # c_suite, vp, director, manager, senior, individual_contributor
    department = Column(
        String(100), nullable=True
    )  # IT, Finance, Supply Chain, HR, Procurement, Operations
    years_in_role = Column(Integer, nullable=True)
    career_history = Column(JSON, default=list)  # [{title, company, duration}]

    # Company
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company_name = Column(String(255), nullable=True)  # denormalized for CSV import ease

    # Decision-Making
    decision_maker_type = Column(
        String(50), nullable=True
    )  # champion, influencer, decision_maker, blocker, user, gatekeeper
    budget_authority = Column(String(50), nullable=True)  # yes, no, unknown
    buying_stage = Column(
        String(50), nullable=True
    )  # unaware, aware, considering, evaluating, purchasing

    # Intelligence (AI-generated)
    pain_points = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    content_topics = Column(JSON, default=list)  # topics they post/engage about
    current_sap_experience = Column(Text, nullable=True)
    ai_profile_summary = Column(Text, nullable=True)
    ai_need_analysis = Column(Text, nullable=True)
    ai_gap_analysis = Column(Text, nullable=True)
    recommended_sap_solutions = Column(JSON, default=list)
    conversation_starters = Column(JSON, default=list)
    best_outreach_channel = Column(String(50), nullable=True)

    # Scoring
    engagement_score = Column(Float, default=0.0)  # 0-100
    fit_score = Column(Float, default=0.0)  # 0-100 — how well they match our ICP
    priority_rank = Column(Integer, nullable=True)

    # Metadata
    tags = Column(JSON, default=list)
    notes = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)  # csv_import, manual, apollo, linkedin

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", backref="stakeholders", lazy="joined")
