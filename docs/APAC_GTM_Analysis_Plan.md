# APAC GTM Country-by-Country Analysis Plan

## Source Data & Ownership

| Source | Sheet(s) | Owner | Description |
|--------|----------|-------|-------------|
| **Country LE Sheets** | AU, SG, IN, Indonesia, TH, MY | Aashita / Ops | Individual country Large Enterprise target lists with SAP install base, customer status, industry, revenue |
| **SAP SEA MOVE LIST** | SAP SEA MOVE LIST -LE | SAP (external) | SAP's own LE definition & MOVE classification. Has own account exec mapping. **Note: SAP's LE definition differs from NTT's** |
| **AMS Active** | AMS (Active SAP Customers) | NTT Data AMS team | NTT Data AMS customers **validated with SAP** - active contracts |
| **AMS Not Active** | AMS (Not Active SAP Cust) | NTT Data AMS team | NTT Data AMS customers **validated with SAP** - not currently active |

## Analysis Approach

### Per Country: TWO separate workstreams

#### 1. LE Analysis (Excel)
- Country sheet data (Aashita/Ops source)
- Cross-referenced with SAP SEA MOVE list (SAP source)
- Track which accounts appear in both (overlap analysis)
- Flag accounts on MOVE list but NOT in country sheet (gaps)
- Flag accounts in country sheet but NOT on MOVE list (NTT-only targets)
- Industry segmentation & revenue tiering
- Customer vs NNN breakdown
- Migration Target vs Managed Services classification

#### 2. AMS Analysis (Excel)
- AMS Active customers per country
- AMS Not Active customers per country
- Contract value analysis
- Pipeline & compete status
- Cross-reference with LE sheet (are AMS customers also LE targets?)

#### 3. GTM PowerPoint (per country)
- Executive summary
- Market landscape (industry breakdown, revenue tiers)
- Target account prioritization
- LE opportunity pipeline
- AMS growth/retention strategy
- Key actions & next steps

## Country Order
1. **Singapore** (starting here)
2. Indonesia
3. Thailand
4. Malaysia
5. India
6. Australia

## Singapore Data Summary (Pre-Analysis)

### SG Sheet (Aashita/Ops)
- **115 accounts** total
- 83 with SAP Install Base / 32 without
- 69 Migration Targets / 14 Managed Services / 32 No SAP
- Urgency: 39 Tier 1, 18 Tier 2, 26 Tier 3, 32 unclassified
- Top industries: BFSI (42), Energy & Utility (25), Wholesale Distribution (13)
- Revenue range: $5B - $433B USD

### SAP SEA MOVE List (SG)
- **75 accounts** on SAP's MOVE list for SG
- 44 first MOVE / 31 second MOVE
- 57 Commercial / 16 Technical / 2 Inactive
- All MA >= $100K
- Top industries: Healthcare (8), Public Sector (7), High Tech (6), Industrial Machinery (6)

### Cross-Reference
- Only **6 accounts overlap** between SG sheet and MOVE list
- This means significant gaps to investigate:
  - 69 SG-only accounts (NTT targets not on SAP MOVE)
  - 109 MOVE-only accounts (SAP flagged but not on NTT SG list)

### AMS (Singapore)
- **0 active** AMS customers
- **16 not-active** AMS customers (Olympus highest at $441K contract value)
- Key names: MAS, BMW Asia, Enterprise Singapore, Mitsubishi Heavy Industries

## Output Files

| Country | LE Excel | AMS Excel | GTM PPT |
|---------|----------|-----------|---------|
| Singapore | `backend/analysis/SG_LE_Analysis.xlsx` | `backend/analysis/SG_AMS_Analysis.xlsx` | `backend/analysis/SG_GTM_Presentation.pptx` |
| Indonesia | `backend/analysis/ID_LE_Analysis.xlsx` | `backend/analysis/ID_AMS_Analysis.xlsx` | `backend/analysis/ID_GTM_Presentation.pptx` |
| Thailand | `backend/analysis/TH_LE_Analysis.xlsx` | `backend/analysis/TH_AMS_Analysis.xlsx` | `backend/analysis/TH_GTM_Presentation.pptx` |
| Malaysia | `backend/analysis/MY_LE_Analysis.xlsx` | `backend/analysis/MY_AMS_Analysis.xlsx` | `backend/analysis/MY_GTM_Presentation.pptx` |
| India | `backend/analysis/IN_LE_Analysis.xlsx` | `backend/analysis/IN_AMS_Analysis.xlsx` | `backend/analysis/IN_GTM_Presentation.pptx` |
| Australia | `backend/analysis/AU_LE_Analysis.xlsx` | `backend/analysis/AU_AMS_Analysis.xlsx` | `backend/analysis/AU_GTM_Presentation.pptx` |
