from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    sub_industry = Column(String(100), nullable=True)
    employee_count = Column(String(50), nullable=True)  # e.g., "1000-5000"
    revenue_range = Column(String(50), nullable=True)  # e.g., "$100M-$500M"
    headquarters_location = Column(String(255), nullable=True)
    regions = Column(JSON, default=list)  # ["EMEA", "NA", "APAC"]

    # SAP Landscape
    current_erp = Column(String(255), nullable=True)  # e.g., "SAP ECC 6.0", "Oracle", "None"
    current_sap_products = Column(JSON, default=list)  # ["S/4HANA", "SuccessFactors"]
    sap_maturity_level = Column(
        String(50), default="unknown"
    )  # none, basic, intermediate, advanced
    digital_transformation_stage = Column(String(50), nullable=True)

    # Intelligence
    known_pain_points = Column(JSON, default=list)
    competitors = Column(JSON, default=list)
    recent_news = Column(JSON, default=list)
    ai_company_analysis = Column(Text, nullable=True)

    # Classification
    priority_tier = Column(Integer, default=3)  # 1=highest, 3=lowest
    tags = Column(JSON, default=list)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
