---
name: ppt-generation
description: "Use this skill to generate PowerPoint presentations from SAP Sales Outreach Engine data. Trigger when the user asks to create a slide deck, pitch deck, presentation, stakeholder briefing, company analysis report, campaign summary, or outreach strategy deck. Also trigger when the user mentions 'PPT', 'PPTX', 'slides', 'deck', or 'presentation' in the context of sales data export."
---

# PPT Generation Skill for SAP Sales Outreach Engine

## Quick Reference

| Task | How |
|------|-----|
| Generate stakeholder briefing deck | `POST /api/presentations/generate` with `type: stakeholder_briefing` |
| Generate company analysis deck | `POST /api/presentations/generate` with `type: company_analysis` |
| Generate campaign summary deck | `POST /api/presentations/generate` with `type: campaign_summary` |
| Generate outreach strategy deck | `POST /api/presentations/generate` with `type: outreach_strategy` |
| Download generated PPTX | `GET /api/presentations/download/{filename}` |

---

## Presentation Types

### 1. Stakeholder Briefing (`stakeholder_briefing`)
Creates a sales-ready briefing deck for a specific stakeholder contact.

**Slides:**
1. Title — stakeholder name, title, company
2. Profile Overview — role, department, seniority, location, LinkedIn summary
3. Need & Gap Analysis — AI-generated pain points and technology gaps
4. SAP Solution Recommendations — matched solutions with fit rationale
5. Engagement Strategy — conversation starters, best channel, recommended approach
6. Key Talking Points & Objection Handling

### 2. Company Analysis (`company_analysis`)
Creates an account intelligence deck for a target company.

**Slides:**
1. Title — company name, industry, tier
2. Company Overview — size, revenue, HQ, industry breakdown
3. Current Technology Landscape — ERP status, SAP maturity, existing products
4. Pain Points & Gaps — identified challenges and missing capabilities
5. SAP Solution Recommendations — prioritized solutions
6. Key Stakeholders — contacts at this company with roles and scores
7. Recommended Approach & Next Steps

### 3. Campaign Summary (`campaign_summary`)
Creates a campaign performance and strategy summary deck.

**Slides:**
1. Title — campaign name, status
2. Campaign Overview — objective, channel, target audience size
3. Target Stakeholder Breakdown — by seniority, department, company
4. SAP Solutions Focus — solutions being positioned
5. Messaging Stats — generated messages, sample content
6. Next Steps & Timeline

### 4. Outreach Strategy (`outreach_strategy`)
Creates a strategic outreach planning deck.

**Slides:**
1. Title — strategy overview
2. Target Audience Segmentation
3. Channel Strategy — LinkedIn vs Email approach
4. Message Framework & Tone Guidelines
5. SAP Solution Positioning
6. Timeline & Milestones

---

## API Usage

### Generate Presentation
```
POST /api/presentations/generate
Content-Type: application/json

{
  "type": "stakeholder_briefing",
  "id": 1,
  "title": "Optional custom title",
  "ai_provider": "ollama"
}
```

Response:
```json
{
  "filename": "stakeholder_briefing_1_20260309.pptx",
  "download_url": "/api/presentations/download/stakeholder_briefing_1_20260309.pptx",
  "slides_count": 6,
  "type": "stakeholder_briefing"
}
```

### Download Presentation
```
GET /api/presentations/download/{filename}
```
Returns the PPTX file.

---

## Design Specifications

### Color Palette (SAP-Inspired Professional)

| Element | Color | Hex |
|---------|-------|-----|
| Primary (dark backgrounds) | SAP Navy | `003366` |
| Secondary (accents) | SAP Blue | `0070F2` |
| Highlight | SAP Gold | `E8A317` |
| Body Background | White | `FFFFFF` |
| Body Text | Dark Gray | `333333` |
| Muted Text | Medium Gray | `666666` |
| Light Background | Ice Blue | `EBF5FB` |

### Typography

| Element | Font | Size | Style |
|---------|------|------|-------|
| Slide Title | Calibri | 36pt | Bold |
| Section Header | Calibri | 24pt | Bold |
| Body Text | Calibri | 14pt | Regular |
| Bullet Points | Calibri | 13pt | Regular |
| Caption/Footer | Calibri | 10pt | Italic |

### Layout Rules
- Minimum 0.5" margins on all slides
- Title slides: dark navy background with white text
- Content slides: white background with navy/blue accents
- Footer on every content slide: "SAP Sales Outreach Engine | Confidential"
- Consistent bullet styling with SAP Blue accent circles

---

## Tech Stack

- **Backend**: `python-pptx` library for PPTX generation
- **AI Content**: Uses the existing AI Engine service for generating slide narratives
- **Data Source**: SQLAlchemy models (Stakeholder, Company, Campaign)
- **Frontend**: React page with type selector, entity picker, and download button

---

## Dependencies

```
pip install python-pptx
```
