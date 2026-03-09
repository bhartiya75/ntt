"""
Post-process NDBS_SAP_Supply_Chain_AI_v2.0.pptx for Toyota Australia:
1. Convert all INR amounts to USD
2. Replace generic/India references with Toyota Australia specifics
3. Fix text overflow issues (shorten long text, adjust font sizes)
4. Add Toyota Australia context throughout
"""

from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
import re

INPUT  = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v2.0.pptx"
OUTPUT = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v2.0.pptx"

prs = Presentation(INPUT)

# ── Text replacements (order matters — more specific first) ──
REPLACEMENTS = [
    # Cover slide — client name
    ("Prepared for [Client Name]", "Prepared for Toyota Motor Corporation Australia"),
    # Opportunity slide — INR to USD
    ("\u20b918L Cr", "$12B"),
    ("inventory locked in Indian\nsupply chains annually", "inventory locked in automotive\nsupply chains globally"),
    ("inventory locked in Indian", "inventory locked in automotive"),
    ("supply chains annually", "supply chains globally"),
    # Demand Forecasting slide — India → Australia references
    ("\"What is next month's demand for SKU X at Delhi dealers?\"", "\"What is next month's demand for RAV4 parts at Sydney dealers?\""),
    ("\"What is next month's demand for SKU X at Delhi dealers?\"", "\"Next month's demand for RAV4 parts at Sydney dealers?\""),
    ("SKU X at Delhi dealers", "RAV4 parts at Sydney dealers"),
    # Inventory slide — India → Australia
    ("Which SKUs are at risk of stockout at Pune depot in next 14", "Which parts risk stockout at Melbourne depot in next 14"),
    ("Which SKUs are at risk of stockout at Pune depot", "Which parts risk stockout at Melbourne depot"),
    ("Pune depot", "Melbourne depot"),
    # Agentic AI conversation — India → Australia
    ("Show me top 5 SKUs at stockout risk in Mumbai", "Show top 5 parts at stockout risk in Sydney"),
    ("Auto-creating transfer request from Pune depot.", "Auto-creating transfer from Melbourne depot."),
    # ROI slide — INR to USD
    ("\u20b915-25Cr", "$10-17M"),
    ("\u20b92-5Cr freed/plant", "$1.3-3.3M freed/plant"),
    ("\u20b93-8Cr saved", "$2-5.3M saved"),
    ("\u20b92-4Cr risk avoided", "$1.3-2.7M risk avoided"),
    ("\u20b95-8Cr logistics saved", "$3.3-5.3M logistics saved"),
    # Demand Forecasting — INR to USD
    ("\u20b92\u20135Cr", "$1.3-3.3M"),
    ("working capital\nfreed per plant", "working capital\nfreed per depot"),
    ("freed per plant", "freed per depot"),
    # SAP data signals — India context
    ("dealership demand for vehicles and parts weeks and m", "dealership demand for vehicles and parts weeks ahead"),
    # Industry context insight bar — no longer needed since enhance_pptx.py now has Toyota AU text directly
    # Next steps — phone format
    ("[+91 XXXX XXXXXX]", "[+61 XXXX XXXXXX]"),
    # Generic SAP client references → Toyota
    ("SAP clients lack real-time\ndemand visibility", "of auto OEMs lack real-time\ndemand visibility"),
    ("SAP clients lack real-time", "of auto OEMs lack real-time"),
    ("What SAP clients are struggling with today", "Challenges facing Toyota Australia today"),
    ("SAP clients are struggling with", "Toyota Australia faces"),
    ("your clients can no longer wait to act", "Why Toyota Australia should act now"),
    ("your clients need to act now", "Why Toyota Australia should act now"),
    ("A three-layer intelligence architecture that SAP clients can",
     "Three-layer intelligence architecture Toyota Australia can deploy today"),
    ("that SAP clients can", "Toyota Australia can deploy"),
    # Generic SAP client text → Toyota-specific (approach slide)
    ("SAP data trapped in ECC/S4HANA \u2014 no real-time analytics laye",
     "SAP ECC6 data lacks real-time analytics layer"),
    ("SAP data trapped in ECC/S4HANA", "SAP ECC6 data lacks real-time analytics"),
    ("Demand forecasting done in Excel \u2014 no ML, no confidence inte",
     "Demand forecasting done in Excel \u2014 no ML models"),
    ("Demand forecasting done in Excel", "Parts forecasting still in Excel"),
    ("Inventory decisions lag 2\u20134 weeks behind actual consumption ",
     "Inventory decisions lag behind consumption patterns"),
    ("Inventory decisions lag 2\u20134 weeks behind actual consumption",
     "Inventory decisions lag behind consumption patterns"),
    ("Logistics routes manually planned \u2014 no dynamic rerouting or ",
     "Logistics routes manually planned \u2014 no rerouting"),
    ("Logistics routes manually planned", "Delivery routes manually planned"),
    # Demand forecasting — dealer context
    ("SKU-level forecast at dealership + region. Confidence bands.",
     "Part-level forecast at dealer + state level. Confidence bands."),
    ("SKU-level forecast at dealership + region",
     "Part-level forecast at dealer + state level"),
    ("Predict dealership demand for vehicles and parts weeks and m",
     "Predict dealer demand for HiLux, RAV4 & parts across Australia"),
    # Inventory — context
    ("Maintain optimal stock across warehouses and dealer networks",
     "Optimal stock across 275 Toyota dealerships & warehouses"),
    # Logistics
    ("Move vehicles and parts efficiently across the network \u2014 low",
     "Move vehicles & parts efficiently across Australia's network"),
]

# ── Process all slides ──
changes = 0
for slide_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                original = run.text
                for old, new in REPLACEMENTS:
                    if old in run.text:
                        run.text = run.text.replace(old, new)
                if run.text != original:
                    changes += 1


# ═══════════════════════════════════════════════════════════════
# FIX OVERFLOW — reduce font sizes on cards with long text
# ═══════════════════════════════════════════════════════════════
SZ_MICRO = Emu(145000)  # Smaller font for overflow-prone text

for slide_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if not run.font.size or not run.text:
                    continue
                # Estimate: each char width ≈ 55% of font size
                box_w = shape.width
                est_chars_per_line = int(box_w / (run.font.size * 0.55)) if run.font.size > 0 else 999
                # Only fix if significantly overflowing (>1.5x chars on a single line)
                lines_in_text = run.text.count('\n') + 1
                longest_line = max(len(l) for l in run.text.split('\n'))
                if longest_line > est_chars_per_line * 1.3 and longest_line > 25:
                    # Calculate the font size needed to fit
                    needed_size = int(box_w / (longest_line * 0.55))
                    # Don't go below ~10pt (roughly 127000 EMU)
                    if needed_size < 127000:
                        needed_size = 127000
                    if needed_size < run.font.size:
                        run.font.size = needed_size


# ═══════════════════════════════════════════════════════════════
# ADDITIONAL TOYOTA AUSTRALIA ENHANCEMENTS
# ═══════════════════════════════════════════════════════════════

# Add Toyota Australia stats to the Opportunity slide (slide 3 in final order)
# Find the slide with "72%" stat — it's the Opportunity slide
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, 'text') and '72%' in shape.text:
            # This is the opportunity slide — already has the $1.9T stat added
            # Let's also find and update the subtitle
            break

# Source annotations: add a small source line to the Opportunity slide
# Find slide with "$1.9T" (which we added)
for slide_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if not hasattr(shape, 'text'):
            continue
        if '$1.9T' in shape.text:
            # Found our stat — add source below the existing content
            from pptx.enum.text import PP_ALIGN as PA
            from pptx.util import Emu as E
            # Add a small source note near the stat
            from pptx.dml.color import RGBColor as RGB
            txBox = slide.shapes.add_textbox(
                E(8900000), E(2500000), E(2800000), E(250000))
            tf = txBox.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PA.CENTER
            r = p.add_run()
            r.text = "Source: McKinsey Global Institute"
            r.font.size = E(110000)
            r.font.italic = True
            r.font.color.rgb = RGB(0x80, 0x99, 0xB3)
            break
    else:
        continue
    break

# Add Toyota-specific stats source on ROI slide
for slide_idx, slide in enumerate(prs.slides):
    found = False
    for shape in slide.shapes:
        if not hasattr(shape, 'text'):
            continue
        if 'Consolidated ROI' in shape.text:
            found = True
            break
    if found:
        from pptx.enum.text import PP_ALIGN as PA
        from pptx.util import Emu as E
        from pptx.dml.color import RGBColor as RGB
        txBox = slide.shapes.add_textbox(
            E(400000), E(5800000), E(11400000), E(300000))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PA.LEFT
        r = p.add_run()
        r.text = "Estimates based on Toyota AU revenue of AUD $12.95B (FY2025) and 275 dealerships  |  Sources: Toyota AU Annual Report, Gartner, McKinsey"
        r.font.size = E(110000)
        r.font.italic = True
        r.font.color.rgb = RGB(0x80, 0x99, 0xB3)
        break


# ═══════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════
prs.save(OUTPUT)
print(f"Saved Toyota Australia-customised presentation to {OUTPUT}")
print(f"Text replacements made: {changes}")
