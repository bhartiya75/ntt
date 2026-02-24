# SAP Sales Outreach Engine

Strategic sales intelligence platform for personalized SAP outreach — 1-to-1 and 1-to-many.

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # add your API keys
python seed_solutions.py
uvicorn app.main:app --reload
```

API docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard at http://localhost:5173

## Features

- **LinkedIn CSV Import** — bulk import contacts from LinkedIn, Sales Nav, or Apollo
- **AI Stakeholder Profiling** — 360° analysis using Claude or OpenAI (needs, gaps, pain points)
- **SAP Solution Matching** — auto-match stakeholders to relevant SAP products
- **1-to-1 Outreach** — deep personalized messages for high-value targets
- **1-to-Many Campaigns** — segment-based scaled outreach with personalization
- **A/B Testing** — generate message variants for optimization
- **Multi-touch Sequences** — automated follow-up message generation

## Configuration

Set these in `backend/.env`:

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes* | Claude API key for AI features |
| `OPENAI_API_KEY` | Yes* | OpenAI API key (alternative) |
| `APOLLO_API_KEY` | No | Apollo.io for contact enrichment |

*At least one AI API key is required for profiling and outreach generation.
