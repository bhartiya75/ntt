from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class SAPSolution(Base):
    __tablename__ = "sap_solutions"

    id = Column(Integer, primary_key=True, index=True)
    solution_name = Column(String(255), nullable=False, unique=True)
    category = Column(
        String(100), nullable=False
    )  # ERP, HCM, Procurement, Analytics, AI, Integration, etc.
    description = Column(Text, nullable=True)

    # Targeting
    target_personas = Column(
        JSON, default=list
    )  # ["CIO", "CFO", "VP IT", "Head of Supply Chain"]
    target_industries = Column(
        JSON, default=list
    )  # ["Manufacturing", "Retail", "Energy"]
    target_company_size = Column(JSON, default=list)  # ["Enterprise", "Mid-Market"]

    # Messaging
    key_value_props = Column(JSON, default=list)
    pain_points_addressed = Column(JSON, default=list)
    competitive_differentiators = Column(JSON, default=list)
    talk_tracks = Column(JSON, default=list)  # proven messaging angles
    case_studies = Column(JSON, default=list)  # [{company, industry, outcome}]
    objection_handlers = Column(JSON, default=list)  # [{objection, response}]

    # Metadata
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
