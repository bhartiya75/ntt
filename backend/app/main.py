"""SAP Sales Outreach Engine — Main Application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.api import stakeholders, companies, campaigns, outreach, import_export, presentations

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Strategic SAP sales intelligence platform for personalized 1-to-1 and 1-to-many outreach",
    version="0.1.0",
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(stakeholders.router, prefix="/api")
app.include_router(companies.router, prefix="/api")
app.include_router(campaigns.router, prefix="/api")
app.include_router(outreach.router, prefix="/api")
app.include_router(import_export.router, prefix="/api")
app.include_router(presentations.router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    import httpx
    ollama_ok = False
    try:
        r = httpx.get(f"{settings.ollama_base_url.replace('/v1', '')}/api/tags", timeout=2)
        ollama_ok = r.status_code == 200
    except Exception:
        pass
    return {
        "status": "healthy",
        "ai_provider": settings.default_ai_provider,
        "ollama_connected": ollama_ok,
        "ollama_model": settings.ollama_model,
    }


@app.get("/api/stats")
def dashboard_stats():
    """Quick stats for the dashboard."""
    from app.database import SessionLocal
    from app.models.stakeholder import Stakeholder
    from app.models.company import Company
    from app.models.campaign import OutreachCampaign
    from app.models.outreach_message import OutreachMessage

    db = SessionLocal()
    try:
        return {
            "total_stakeholders": db.query(Stakeholder).count(),
            "total_companies": db.query(Company).count(),
            "total_campaigns": db.query(OutreachCampaign).count(),
            "active_campaigns": db.query(OutreachCampaign)
            .filter(OutreachCampaign.status == "active")
            .count(),
            "total_messages": db.query(OutreachMessage).count(),
            "messages_sent": db.query(OutreachMessage)
            .filter(OutreachMessage.status == "sent")
            .count(),
            "replies_received": db.query(OutreachMessage)
            .filter(OutreachMessage.status == "replied")
            .count(),
        }
    finally:
        db.close()
