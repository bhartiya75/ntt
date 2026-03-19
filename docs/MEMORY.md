# NTT Project Memory — Persistent Context

> Auto-loaded at session start. Last updated: 2026-03-19.

## Project Identity

- **Name**: NTT SAP Sales Outreach Engine
- **Owner**: bhartiya75 (Chandra Shekhar Bhartiya)
- **Repo**: github.com/bhartiya75/ntt
- **Purpose**: Strategic sales intelligence platform for NTT DATA's SAP services outreach across APAC

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy ORM, SQLite (dev) / PostgreSQL (prod)
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite
- **AI**: Ollama (local LLM, switched from Claude/OpenAI APIs for dev)
- **PPT Generation**: python-pptx library
- **Package Manager**: pip (backend), npm (frontend)

## Architecture

```
ntt/
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── models/    # SQLAlchemy models (stakeholder, company, campaign, outreach, sap_solution)
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── api/       # REST endpoints (stakeholders, companies, campaigns, outreach, import/export, presentations)
│   │   ├── services/  # Business logic (ai_engine, ppt_generator, profiling, enrichment, sap_matcher, segmentation, outreach_generator)
│   │   └── data/      # sap_solutions.json knowledge base
│   ├── generated_ppts/  # Output PPTs
│   └── Consolidated LE APAC.xlsx  # Key data file — APAC legal entity financials
├── frontend/          # React + Vite + Tailwind
│   └── src/pages/     # Dashboard, Companies, Stakeholders, Campaigns, Outreach, Presentations, Import
├── scripts/           # PPT generation scripts (seatrium, toyota)
├── docs/              # Generated PPTs + reports
└── .mcp.json          # MCP servers (claude-flow, jcodemunch, memento)
```

## Key Data Files

- **Consolidated LE APAC.xlsx**: Financial data for APAC legal entities — revenue, margins, headcount
- **OEP Pegasus Archival_.pdf**: Seatrium's OEP Pegasus archival project documentation
- **sap_solutions.json**: SAP solution knowledge base for matching to stakeholders

## Completed Work (Chronological)

1. **SAP Sales Outreach Engine scaffold** — Full FastAPI + React app with models, schemas, APIs, services
2. **Switched to Ollama** — Local LLM instead of cloud APIs, added demo seed data
3. **PPT generation skill** — Full-stack PPTX generation from sales/campaign data
4. **Toyota Australia AI use cases** — Custom PPT with industry-specific AI use cases, USD formatting, source citations
5. **NDBS SAP Supply Chain AI v2.0** — Enhanced presentation with demos and overflow fixes
6. **Seatrium SAP Pegasus migration briefing** — 7-slide 16:9 deck, NTT DATA blue theme, covering ECC→S/4HANA migration
7. **Consolidated LE APAC Excel upload** — Financial data for analysis
8. **Memory persistence research** — Two documents on multi-layer AI agent memory architecture

## Architecture Decisions

- **Decision**: Use Ollama for local LLM (was Claude/OpenAI APIs)
  - Reason: Dev environment flexibility, no API key dependency
- **Decision**: python-pptx for PPT generation (not Google Slides or cloud)
  - Reason: Offline, full control over formatting, NTT DATA brand compliance
- **Decision**: SQLite for dev, PostgreSQL for prod
  - Reason: Zero-config dev, production-ready scaling
- **Decision**: Multi-layer memory architecture (5 layers)
  - Reason: Session amnesia is blocking productivity; need persistent context

## Active Clients / Targets

- **Seatrium**: SAP ECC → S/4HANA Pegasus migration, Singapore-based marine/offshore
- **Toyota Australia**: AI use cases across supply chain, quality, predictive maintenance
- **APAC Legal Entities**: Consolidated financial analysis from Excel data

## Known Gotchas

- PPT color scheme: NTT DATA blue (#0070F2), Navy (#003366), Gold (#E8A317)
- Generated PPTs go to `backend/generated_ppts/` or `docs/`
- The frontend expects API at `http://localhost:8000` (configured in vite proxy)
- Excel file has spaces in name: "Consolidated LE APAC.xlsx"
- Branch naming: feature branches must start with `claude/` and include session ID

## Conventions

- Backend follows FastAPI patterns: routers in `api/`, Pydantic schemas in `schemas/`
- Services handle business logic, not API routes
- PPT slides: 16:9 aspect ratio, NTT DATA branding, professional tone
- All scripts go in `scripts/` directory
- Use `docs/` for generated outputs and reports

## Current Branch

- Working branch: `claude/seatrium-sap-slides-lSKeB`
- Other branches: `claude/sap-sales-outreach-engine-oGVmJ` (has memory docs), `claude/ppt-generation-skill-BZ89S`

## Pending Tasks

- Analysis of Consolidated LE APAC.xlsx financial data
- More client-specific presentation generation
- Frontend refinement and testing
- Memory system full deployment (5 layers)
