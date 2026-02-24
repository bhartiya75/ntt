# SAP Sales Outreach Engine

Strategic sales intelligence platform for personalized SAP outreach — 1-to-1 and 1-to-many.

**Runs 100% locally** using Ollama for AI — no cloud API keys needed.

## Quick Start

### 1. Install & Start Ollama (Local LLM)

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
ollama serve  # keep running in background
```

### 2. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed_solutions.py   # load SAP knowledge base
python seed_demo_data.py   # load sample stakeholders & companies
uvicorn app.main:app --reload
```

API docs at http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard at http://localhost:5173

## Features

- **Local AI (Ollama)** — all AI features run on your machine, no API keys needed
- **LinkedIn CSV Import** — bulk import contacts from LinkedIn, Sales Nav, or Apollo
- **AI Stakeholder Profiling** — 360° analysis (needs, gaps, pain points, conversation starters)
- **SAP Solution Matching** — auto-match stakeholders to relevant SAP products
- **1-to-1 Outreach** — deep personalized messages for high-value targets
- **1-to-Many Campaigns** — segment-based scaled outreach with personalization
- **A/B Testing** — generate message variants for optimization
- **Multi-touch Sequences** — automated follow-up message generation

## AI Providers

The engine supports 3 AI providers. Set `DEFAULT_AI_PROVIDER` in `backend/.env`:

| Provider | Config | Description |
|----------|--------|-------------|
| `ollama` (default) | `OLLAMA_BASE_URL`, `OLLAMA_MODEL` | Local LLM via Ollama — no API keys, full privacy |
| `claude` | `ANTHROPIC_API_KEY` | Anthropic Claude API (cloud) |
| `openai` | `OPENAI_API_KEY` | OpenAI GPT API (cloud) |

You can also swap in your own fine-tuned model (RAG/LoRA trained) via any OpenAI-compatible API endpoint.

## Configuration

Set these in `backend/.env`:

| Variable | Required | Description |
|----------|----------|-------------|
| `DEFAULT_AI_PROVIDER` | No | `ollama` (default), `claude`, or `openai` |
| `OLLAMA_BASE_URL` | No | Ollama API URL (default: `http://localhost:11434/v1`) |
| `OLLAMA_MODEL` | No | Ollama model name (default: `qwen2.5:7b`) |
| `ANTHROPIC_API_KEY` | No | Only needed if using `claude` provider |
| `OPENAI_API_KEY` | No | Only needed if using `openai` provider |
| `APOLLO_API_KEY` | No | Apollo.io for contact enrichment |
