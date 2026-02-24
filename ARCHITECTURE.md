# SAP Sales Outreach Engine — Architecture & Plan

## Overview

A strategic sales intelligence platform for SAP services outreach. It profiles LinkedIn stakeholders, identifies their pain points and needs, and generates hyper-personalized outreach plans — both 1-to-1 and 1-to-many.

**Core Focus:** SAP Business AI and full SAP portfolio (S/4HANA, BTP, SuccessFactors, Ariba, Analytics, Integration Suite, Signavio, etc.)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Dashboard)                │
│  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────┐ │
│  │Stakeholder│ │  Campaign     │ │ Outreach │ │  Analytics │ │
│  │ Profiles  │ │  Manager      │ │ Drafts   │ │  & Reports │ │
│  └──────────┘ └──────────────┘ └──────────┘ └────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │ REST API
┌───────────────────────┴─────────────────────────────────────┐
│                  FastAPI Backend                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. DATA INGESTION LAYER                            │    │
│  │     ├── CSV Import (LinkedIn exports, Sales Nav)    │    │
│  │     ├── Enrichment APIs (Apollo, Clearbit)          │    │
│  │     └── Manual Entry / CRM Sync                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2. STAKEHOLDER PROFILING ENGINE                    │    │
│  │     ├── Role & Seniority Analysis                   │    │
│  │     ├── Company Technographics (current SAP usage)  │    │
│  │     ├── Pain Point Detection                        │    │
│  │     ├── Decision-Maker Mapping                      │    │
│  │     └── Engagement History Tracking                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  3. AI ANALYSIS ENGINE (Claude + OpenAI)            │    │
│  │     ├── Profile Summarization                       │    │
│  │     ├── Need/Gap Analysis per Stakeholder           │    │
│  │     ├── SAP Solution Matching                       │    │
│  │     └── Competitive Intelligence                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  4. OUTREACH ENGINE                                 │    │
│  │     ├── 1-to-1: Deep personalized messages          │    │
│  │     ├── 1-to-Many: Segment-based campaigns          │    │
│  │     ├── Multi-channel: LinkedIn, Email, InMail      │    │
│  │     ├── Sequence Builder (multi-touch)              │    │
│  │     └── A/B Message Variants                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  5. CAMPAIGN MANAGEMENT                             │    │
│  │     ├── Campaign Creation & Scheduling              │    │
│  │     ├── Stakeholder Segmentation                    │    │
│  │     ├── Response Tracking                           │    │
│  │     └── Pipeline Stage Management                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Database: SQLite (dev) → PostgreSQL (prod)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Model

### Stakeholder (Contact)
```
- id, full_name, first_name, last_name
- linkedin_url, linkedin_headline, linkedin_summary
- email, phone
- job_title, seniority_level (C-Suite, VP, Director, Manager, IC)
- department (IT, Finance, Supply Chain, HR, Procurement, etc.)
- company_id (FK)
- decision_maker_type (Champion, Influencer, Decision Maker, Blocker, User)
- pain_points[] — AI-detected from profile + company context
- interests[] — extracted from LinkedIn activity
- current_sap_experience — what SAP products they've used
- ai_profile_summary — Claude/OpenAI generated profile analysis
- engagement_score (0-100)
- tags[], notes
- created_at, updated_at
```

### Company (Account)
```
- id, name, domain, industry, sub_industry
- employee_count, revenue_range
- headquarters_location, regions[]
- current_erp — what ERP/systems they use today
- current_sap_products[] — existing SAP footprint
- sap_maturity_level (None, Basic, Intermediate, Advanced)
- digital_transformation_stage
- known_pain_points[]
- ai_company_analysis — AI-generated company intelligence
- priority_tier (Tier 1, 2, 3)
- tags[], notes
- created_at, updated_at
```

### OutreachCampaign
```
- id, name, description
- campaign_type (one_to_one, one_to_many)
- target_segment — description of who this targets
- sap_solution_focus[] — which SAP products to pitch
- value_proposition — core message
- channel (linkedin_message, linkedin_inmail, email, multi_channel)
- sequence_steps[] — multi-touch sequence definition
- status (draft, active, paused, completed)
- stakeholder_ids[] or segment_filter
- created_at, updated_at
```

### OutreachMessage
```
- id, campaign_id (FK), stakeholder_id (FK)
- channel, sequence_step_number
- subject, body
- personalization_context — what AI used to personalize
- variant (A/B testing)
- status (draft, approved, sent, replied, bounced)
- sent_at, opened_at, replied_at
- ai_model_used (claude, openai)
- created_at
```

### SAP Solution Library
```
- id, solution_name (e.g., "SAP Business AI", "S/4HANA Cloud")
- category (ERP, HCM, Procurement, Analytics, AI, Integration, etc.)
- target_personas[] — which roles care about this
- target_industries[]
- key_value_props[]
- pain_points_addressed[]
- competitive_differentiators[]
- talk_tracks[] — proven messaging angles
- case_studies[] — reference stories
```

---

## Stakeholder Profiling — What We Analyze

For each stakeholder, the AI engine builds a **360° profile**:

### 1. Professional Context
- Current role, responsibilities, reporting structure
- Career trajectory (promotions, lateral moves, industry changes)
- Skills and endorsements (technical vs. business)
- Content they share/engage with on LinkedIn

### 2. Company Context
- Company's current tech stack and SAP footprint
- Industry-specific challenges and trends
- Digital transformation maturity
- Recent news (M&A, leadership changes, earnings)

### 3. Need & Gap Analysis (AI-Powered)
- **What they likely need** — based on role + company + industry
- **What's missing** — gaps in their current SAP landscape
- **What they'd value** — based on content engagement and interests
- **Buying signals** — job postings, tech stack changes, events attended
- **Risk factors** — competitor relationships, recent vendor switches

### 4. Engagement Strategy
- Best channel to reach them
- Optimal timing and frequency
- Conversation starters (shared connections, mutual interests, recent posts)
- SAP solutions most relevant to their specific situation

---

## Outreach Strategy

### 1-to-1 (High-Touch)
For Tier 1 accounts and senior decision-makers:
- Deep research per individual
- Highly personalized message referencing their specific context
- Multi-touch sequence (connect → value → insight → ask)
- Custom SAP Business AI use cases for their industry/role

### 1-to-Many (Scaled)
For broader segments:
- Segment by: industry + role + SAP maturity + pain point
- Personalized at segment level with individual variable insertion
- Campaign themes tied to SAP Business AI value stories
- Automated sequences with manual review gates

### Message Framework
```
1. Hook       — Reference something specific to them (post, company news, role)
2. Relevance  — Connect their situation to a SAP challenge/opportunity
3. Value      — Share an insight, not a pitch (industry trend, peer benchmark)
4. Proof      — Brief reference to similar company/success
5. Ask        — Soft CTA (thoughts? worth a conversation? quick call?)
```

---

## Tech Stack

| Layer           | Technology                          |
|-----------------|-------------------------------------|
| Backend         | Python 3.11+, FastAPI               |
| Frontend        | React 18, TypeScript, Tailwind CSS  |
| Database        | SQLAlchemy ORM, SQLite → PostgreSQL |
| AI — Primary    | Anthropic Claude API (claude-sonnet) |
| AI — Secondary  | OpenAI API (gpt-4o) — for variety   |
| Data Enrichment | Apollo.io API, Clearbit (optional)  |
| LinkedIn Import | CSV import + manual enrichment      |
| Task Queue      | Background tasks via FastAPI         |
| Auth            | JWT-based simple auth               |

---

## Project Structure

```
ntt/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Settings & env vars
│   │   ├── database.py             # DB connection & session
│   │   ├── models/
│   │   │   ├── stakeholder.py
│   │   │   ├── company.py
│   │   │   ├── campaign.py
│   │   │   ├── outreach_message.py
│   │   │   └── sap_solution.py
│   │   ├── schemas/                # Pydantic request/response
│   │   │   ├── stakeholder.py
│   │   │   ├── company.py
│   │   │   ├── campaign.py
│   │   │   └── outreach.py
│   │   ├── api/
│   │   │   ├── stakeholders.py     # CRUD + search
│   │   │   ├── companies.py
│   │   │   ├── campaigns.py
│   │   │   ├── outreach.py
│   │   │   └── import_export.py    # CSV import
│   │   ├── services/
│   │   │   ├── profiling.py        # Stakeholder analysis
│   │   │   ├── ai_engine.py        # Claude + OpenAI integration
│   │   │   ├── outreach_generator.py  # Message generation
│   │   │   ├── enrichment.py       # Apollo/Clearbit integration
│   │   │   ├── segmentation.py     # Audience segmentation
│   │   │   └── sap_matcher.py      # Match stakeholders to SAP solutions
│   │   └── data/
│   │       └── sap_solutions.json  # SAP solution knowledge base
│   ├── requirements.txt
│   └── alembic/                    # DB migrations
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
├── ARCHITECTURE.md
└── README.md
```

---

## Implementation Phases

### Phase 1 — Foundation (Current)
- [x] Architecture design
- [ ] Project scaffold (FastAPI + React)
- [ ] Database models & migrations
- [ ] CSV import for LinkedIn data
- [ ] Basic stakeholder & company CRUD

### Phase 2 — Intelligence
- [ ] AI profiling engine (Claude + OpenAI)
- [ ] SAP solution knowledge base
- [ ] Stakeholder need/gap analysis
- [ ] Company technographic analysis

### Phase 3 — Outreach
- [ ] 1-to-1 message generation
- [ ] 1-to-many campaign builder
- [ ] Multi-touch sequence engine
- [ ] A/B variant generation

### Phase 4 — Dashboard
- [ ] React frontend
- [ ] Stakeholder profiles view
- [ ] Campaign management UI
- [ ] Analytics & reporting

### Phase 5 — Scale
- [ ] Enrichment API integrations
- [ ] Response tracking
- [ ] Pipeline management
- [ ] Export to LinkedIn / email tools
