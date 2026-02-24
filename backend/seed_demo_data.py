"""Seed script to load demo stakeholders and companies for testing."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.stakeholder import Stakeholder
from app.models.company import Company

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Companies ---
companies_data = [
    {
        "name": "Siemens AG",
        "domain": "siemens.com",
        "industry": "Industrial Manufacturing",
        "sub_industry": "Automation & Digitalization",
        "employee_count": "300,000+",
        "revenue_range": "$70B+",
        "headquarters_location": "Munich, Germany",
        "regions": ["EMEA", "Americas", "APAC"],
        "current_erp": "SAP ECC 6.0",
        "current_sap_products": ["SAP ECC", "SAP BW", "SAP Ariba"],
        "sap_maturity_level": "Intermediate",
        "digital_transformation_stage": "Accelerating",
        "known_pain_points": [
            "Legacy ECC migration to S/4HANA",
            "Disconnected factory floor systems",
            "Manual procurement processes at scale",
        ],
        "priority_tier": 1,
        "tags": ["strategic", "manufacturing", "s4hana-migration"],
    },
    {
        "name": "Unilever",
        "domain": "unilever.com",
        "industry": "Consumer Goods",
        "sub_industry": "FMCG",
        "employee_count": "148,000",
        "revenue_range": "$60B+",
        "headquarters_location": "London, UK",
        "regions": ["EMEA", "Americas", "APAC"],
        "current_erp": "Mixed (SAP + Oracle)",
        "current_sap_products": ["SAP S/4HANA", "SAP Ariba", "SAP IBP"],
        "sap_maturity_level": "Advanced",
        "digital_transformation_stage": "Leading",
        "known_pain_points": [
            "Harmonizing global SAP instances",
            "Supply chain visibility across 190 countries",
            "Sustainability reporting & ESG data",
        ],
        "priority_tier": 1,
        "tags": ["strategic", "consumer-goods", "global"],
    },
    {
        "name": "Deutsche Bank",
        "domain": "db.com",
        "industry": "Financial Services",
        "sub_industry": "Banking",
        "employee_count": "87,000",
        "revenue_range": "$30B+",
        "headquarters_location": "Frankfurt, Germany",
        "regions": ["EMEA", "Americas", "APAC"],
        "current_erp": "SAP ECC with custom extensions",
        "current_sap_products": ["SAP ECC", "SAP SuccessFactors", "SAP Concur"],
        "sap_maturity_level": "Intermediate",
        "digital_transformation_stage": "Transforming",
        "known_pain_points": [
            "Regulatory compliance automation",
            "HR transformation across global offices",
            "Real-time financial reporting",
        ],
        "priority_tier": 1,
        "tags": ["financial-services", "compliance", "hr-transformation"],
    },
    {
        "name": "BMW Group",
        "domain": "bmwgroup.com",
        "industry": "Automotive",
        "sub_industry": "OEM Manufacturing",
        "employee_count": "149,000",
        "revenue_range": "$150B+",
        "headquarters_location": "Munich, Germany",
        "regions": ["EMEA", "Americas", "APAC"],
        "current_erp": "SAP S/4HANA (partial rollout)",
        "current_sap_products": ["SAP S/4HANA", "SAP BTP", "SAP Ariba", "SAP Analytics Cloud"],
        "sap_maturity_level": "Advanced",
        "digital_transformation_stage": "Leading",
        "known_pain_points": [
            "EV supply chain complexity",
            "Integrating factory IoT data with ERP",
            "Predictive maintenance analytics",
        ],
        "priority_tier": 1,
        "tags": ["automotive", "innovation", "iot"],
    },
    {
        "name": "Tata Consultancy Services",
        "domain": "tcs.com",
        "industry": "IT Services",
        "sub_industry": "Consulting & SI",
        "employee_count": "600,000+",
        "revenue_range": "$28B+",
        "headquarters_location": "Mumbai, India",
        "regions": ["APAC", "EMEA", "Americas"],
        "current_erp": "SAP S/4HANA",
        "current_sap_products": ["SAP S/4HANA", "SAP SuccessFactors", "SAP BTP"],
        "sap_maturity_level": "Advanced",
        "digital_transformation_stage": "Leading",
        "known_pain_points": [
            "Managing 600K+ employee lifecycle",
            "Global workforce planning",
            "Client project analytics at scale",
        ],
        "priority_tier": 2,
        "tags": ["it-services", "partner-potential", "successfactors"],
    },
    {
        "name": "Maersk",
        "domain": "maersk.com",
        "industry": "Logistics & Transportation",
        "sub_industry": "Shipping & Logistics",
        "employee_count": "100,000",
        "revenue_range": "$50B+",
        "headquarters_location": "Copenhagen, Denmark",
        "regions": ["EMEA", "Americas", "APAC"],
        "current_erp": "Mixed legacy systems",
        "current_sap_products": ["SAP ECC"],
        "sap_maturity_level": "Basic",
        "digital_transformation_stage": "Accelerating",
        "known_pain_points": [
            "End-to-end supply chain digitization",
            "Legacy system consolidation",
            "Real-time container tracking integration",
        ],
        "priority_tier": 1,
        "tags": ["logistics", "greenfield-opportunity", "digital-transformation"],
    },
]

company_map = {}
for c_data in companies_data:
    existing = db.query(Company).filter(Company.name == c_data["name"]).first()
    if existing:
        company_map[c_data["name"]] = existing.id
        print(f"  Company exists: {c_data['name']}")
        continue
    company = Company(**c_data)
    db.add(company)
    db.flush()
    company_map[c_data["name"]] = company.id
    print(f"  Added company: {c_data['name']}")

# --- Stakeholders ---
stakeholders_data = [
    {
        "full_name": "Klaus Weber",
        "first_name": "Klaus",
        "last_name": "Weber",
        "email": "k.weber@siemens.com",
        "job_title": "VP of Digital Transformation",
        "seniority_level": "VP",
        "department": "IT",
        "company_name": "Siemens AG",
        "linkedin_headline": "Leading Digital Transformation at Siemens | Industry 4.0 | SAP & Cloud",
        "linkedin_summary": "20+ years driving enterprise technology transformation in manufacturing. Currently leading Siemens digital factory initiative. Previously held CTO roles at major industrial firms. Passionate about Industry 4.0, IoT, and AI-driven manufacturing.",
        "linkedin_location": "Munich, Germany",
        "decision_maker_type": "Decision Maker",
        "budget_authority": "Approves $10M+",
        "interests": ["Industry 4.0", "Digital Twin", "Cloud ERP", "AI in Manufacturing"],
        "content_topics": ["Smart Factory", "SAP S/4HANA", "Digital Supply Chain"],
        "current_sap_experience": "SAP ECC power user, evaluating S/4HANA migration",
        "tags": ["high-priority", "decision-maker", "s4hana"],
        "source": "Sales Navigator",
    },
    {
        "full_name": "Sarah Chen",
        "first_name": "Sarah",
        "last_name": "Chen",
        "email": "sarah.chen@unilever.com",
        "job_title": "Global Head of Supply Chain Technology",
        "seniority_level": "Director",
        "department": "Supply Chain",
        "company_name": "Unilever",
        "linkedin_headline": "Transforming Global Supply Chains through Technology & Analytics | Unilever",
        "linkedin_summary": "Leading technology strategy for Unilever's global supply chain across 190+ countries. Focus on predictive analytics, sustainability tech, and end-to-end visibility. MBA from INSEAD, 15 years in CPG supply chain.",
        "linkedin_location": "London, UK",
        "decision_maker_type": "Champion",
        "budget_authority": "Influences $5M+",
        "interests": ["Supply Chain Analytics", "Sustainability", "AI/ML", "Planning & Forecasting"],
        "content_topics": ["Sustainable Supply Chain", "Demand Sensing", "SAP IBP"],
        "current_sap_experience": "SAP IBP, SAP Ariba — looking to expand analytics",
        "tags": ["champion", "supply-chain", "analytics"],
        "source": "LinkedIn",
    },
    {
        "full_name": "Michael Hartmann",
        "first_name": "Michael",
        "last_name": "Hartmann",
        "email": "m.hartmann@db.com",
        "job_title": "Chief Information Officer",
        "seniority_level": "C-Suite",
        "department": "IT",
        "company_name": "Deutsche Bank",
        "linkedin_headline": "CIO at Deutsche Bank | Banking Technology | Digital Transformation",
        "linkedin_summary": "CIO driving technology modernization across Deutsche Bank. Focus areas: cloud migration, regulatory technology, AI-powered risk management, and core banking transformation. Previously VP Engineering at Goldman Sachs.",
        "linkedin_location": "Frankfurt, Germany",
        "decision_maker_type": "Decision Maker",
        "budget_authority": "Approves $50M+",
        "interests": ["RegTech", "Cloud Migration", "Core Banking", "AI Risk"],
        "content_topics": ["Banking Transformation", "Cloud Native", "Regulatory AI"],
        "current_sap_experience": "SAP ECC for financials, SuccessFactors for HR",
        "tags": ["c-suite", "high-priority", "banking"],
        "source": "Conference",
    },
    {
        "full_name": "Priya Sharma",
        "first_name": "Priya",
        "last_name": "Sharma",
        "email": "priya.sharma@bmwgroup.com",
        "job_title": "Head of Enterprise Architecture",
        "seniority_level": "Director",
        "department": "IT",
        "company_name": "BMW Group",
        "linkedin_headline": "Enterprise Architecture | SAP S/4HANA | BTP | BMW Group",
        "linkedin_summary": "Leading enterprise architecture at BMW Group. Driving SAP S/4HANA rollout across 30+ plants. Deep expertise in SAP BTP, integration architecture, and automotive ERP. Speaker at SAP TechEd.",
        "linkedin_location": "Munich, Germany",
        "decision_maker_type": "Influencer",
        "budget_authority": "Recommends $10M+",
        "interests": ["Enterprise Architecture", "SAP BTP", "Integration", "Automotive Tech"],
        "content_topics": ["SAP S/4HANA Migration", "BTP Extensions", "API-First Architecture"],
        "current_sap_experience": "Deep SAP S/4HANA and BTP expertise, SAP Mentor",
        "tags": ["influencer", "sap-expert", "architect"],
        "source": "SAP TechEd",
    },
    {
        "full_name": "James Richardson",
        "first_name": "James",
        "last_name": "Richardson",
        "email": "j.richardson@tcs.com",
        "job_title": "Global Practice Head - SAP",
        "seniority_level": "VP",
        "department": "Consulting",
        "company_name": "Tata Consultancy Services",
        "linkedin_headline": "SAP Practice Head at TCS | S/4HANA | RISE with SAP | 25K+ SAP consultants",
        "linkedin_summary": "Leading TCS's global SAP practice with 25,000+ consultants. Driving client transformation using RISE with SAP, S/4HANA Cloud, and SAP Business AI. 18 years of SAP consulting experience.",
        "linkedin_location": "Mumbai, India",
        "decision_maker_type": "Influencer",
        "budget_authority": "Influences partner investments",
        "interests": ["RISE with SAP", "SAP Business AI", "Cloud Transformation", "Partner Ecosystem"],
        "content_topics": ["SAP Partner Strategy", "Cloud Migration Factory", "AI in ERP"],
        "current_sap_experience": "Expert — leads 25K+ SAP team",
        "tags": ["partner", "sap-expert", "strategic-alliance"],
        "source": "SAP Partner Summit",
    },
    {
        "full_name": "Emma Johansson",
        "first_name": "Emma",
        "last_name": "Johansson",
        "email": "emma.johansson@maersk.com",
        "job_title": "SVP Technology & Digital",
        "seniority_level": "VP",
        "department": "IT",
        "company_name": "Maersk",
        "linkedin_headline": "SVP Technology at Maersk | Logistics Tech | Digital Transformation | Cloud",
        "linkedin_summary": "Driving Maersk's technology transformation from legacy systems to cloud-native. Leading a team of 2,000+ engineers. Focus on real-time logistics platform, API ecosystem, and data-driven operations.",
        "linkedin_location": "Copenhagen, Denmark",
        "decision_maker_type": "Decision Maker",
        "budget_authority": "Approves $20M+",
        "interests": ["Cloud Migration", "API Platform", "Real-time Logistics", "Data Analytics"],
        "content_topics": ["Logistics 4.0", "Cloud Transformation", "Platform Engineering"],
        "current_sap_experience": "Legacy SAP ECC — greenfield S/4HANA opportunity",
        "tags": ["decision-maker", "greenfield", "high-priority"],
        "source": "Sales Navigator",
    },
    {
        "full_name": "Raj Patel",
        "first_name": "Raj",
        "last_name": "Patel",
        "email": "raj.patel@siemens.com",
        "job_title": "Director of Procurement",
        "seniority_level": "Director",
        "department": "Procurement",
        "company_name": "Siemens AG",
        "linkedin_headline": "Director of Procurement at Siemens | Strategic Sourcing | SAP Ariba",
        "linkedin_summary": "Leading procurement transformation at Siemens with focus on strategic sourcing, supplier risk management, and sustainability. Implementing SAP Ariba across 100+ buying entities.",
        "linkedin_location": "Munich, Germany",
        "decision_maker_type": "Champion",
        "budget_authority": "Influences $5M+",
        "interests": ["Strategic Sourcing", "Supplier Risk", "Procurement Analytics", "ESG"],
        "content_topics": ["SAP Ariba", "Procurement Best Practices", "Supplier Diversity"],
        "current_sap_experience": "SAP Ariba expert — expanding to SAP Business Network",
        "tags": ["champion", "procurement", "ariba"],
        "source": "LinkedIn",
    },
    {
        "full_name": "Lisa Müller",
        "first_name": "Lisa",
        "last_name": "Müller",
        "email": "l.mueller@bmwgroup.com",
        "job_title": "CHRO",
        "seniority_level": "C-Suite",
        "department": "HR",
        "company_name": "BMW Group",
        "linkedin_headline": "CHRO at BMW Group | Future of Work | People Analytics | SuccessFactors",
        "linkedin_summary": "CHRO leading BMW's HR transformation. Focused on employee experience, people analytics, and workforce planning for the EV era. Implementing SAP SuccessFactors globally.",
        "linkedin_location": "Munich, Germany",
        "decision_maker_type": "Decision Maker",
        "budget_authority": "Approves $15M+",
        "interests": ["People Analytics", "Employee Experience", "Workforce Planning", "HR AI"],
        "content_topics": ["Future of Work", "SuccessFactors", "HR Technology"],
        "current_sap_experience": "SAP SuccessFactors — evaluating AI add-ons",
        "tags": ["c-suite", "hr", "successfactors"],
        "source": "SAP SuccessConnect",
    },
]

count = 0
for s_data in stakeholders_data:
    existing = db.query(Stakeholder).filter(
        Stakeholder.full_name == s_data["full_name"],
        Stakeholder.company_name == s_data["company_name"],
    ).first()
    if existing:
        print(f"  Stakeholder exists: {s_data['full_name']}")
        continue

    # Link to company
    company_name = s_data.get("company_name", "")
    if company_name in company_map:
        s_data["company_id"] = company_map[company_name]

    stakeholder = Stakeholder(**s_data)
    db.add(stakeholder)
    count += 1
    print(f"  Added stakeholder: {s_data['full_name']} ({s_data['job_title']} at {company_name})")

db.commit()
db.close()

print(f"\nSeeded {len(companies_data)} companies and {count} stakeholders.")
