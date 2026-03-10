"""
Enhance NDBS_SAP_Supply_Chain_AI_v1.1.pptx
- Add 6 new slides (Agenda, Industry Context, Tech Stack, ROI Summary, Roadmap, Next Steps)
- Edit 5 existing slides (Cover, Opportunity, Demand Forecasting, Logistics, Agentic AI)
- Output: NDBS_SAP_Supply_Chain_AI_v2.0.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from copy import deepcopy
from lxml import etree
import os

# ── Color Palette (from existing deck) ──
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BLUE  = RGBColor(0xB8, 0xCF, 0xE8)
NEAR_WHITE  = RGBColor(0xE8, 0xF4, 0xFD)
CYAN_ACCENT = RGBColor(0x50, 0xE6, 0xFF)
MS_BLUE     = RGBColor(0x00, 0x78, 0xD4)
AMBER       = RGBColor(0xFF, 0xB9, 0x00)
GREEN       = RGBColor(0x00, 0xB2, 0x94)
ORANGE      = RGBColor(0xFF, 0x8C, 0x00)
DARK_BG     = RGBColor(0x0A, 0x16, 0x28)
DARK_CARD   = RGBColor(0x0F, 0x1F, 0x38)
DARKER_CARD = RGBColor(0x12, 0x25, 0x40)

# ── Font sizes (EMU) ──
SZ_TITLE    = 440309
SZ_SUBTITLE = 220091
SZ_BODY     = 203200
SZ_SMALL    = 186309
SZ_TINY     = 169291
SZ_NUMBER   = 304800
SZ_BIG_STAT = 575691
SZ_MED_STAT = 372491

SLIDE_W = 12192000
SLIDE_H = 6858000


def add_textbox(slide, left, top, width, height, text, font_size=SZ_BODY,
                bold=False, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT,
                font_name=None):
    """Add a textbox with a single run."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if font_name:
        run.font.name = font_name
    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines, default_size=SZ_BODY,
                          default_color=LIGHT_BLUE, alignment=PP_ALIGN.LEFT):
    """Add textbox with multiple paragraphs. lines = [(text, size, bold, color), ...]"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line_data in enumerate(lines):
        text = line_data[0]
        size = line_data[1] if len(line_data) > 1 else default_size
        bold = line_data[2] if len(line_data) > 2 else False
        color = line_data[3] if len(line_data) > 3 else default_color
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = alignment
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = text
        run.font.size = size
        run.font.bold = bold
        run.font.color.rgb = color
    return txBox


def add_rounded_rect(slide, left, top, width, height, fill_color=DARK_CARD):
    """Add a rounded rectangle shape with solid fill."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_circle(slide, left, top, size, fill_color):
    """Add a circle shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_chevron_arrow(slide, left, top, width, height, fill_color=MS_BLUE):
    """Add a chevron/arrow shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def set_slide_bg(slide, color=DARK_BG):
    """Set solid background color on a slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def duplicate_slide(prs, source_idx):
    """Duplicate a slide by copying its XML. Returns the new slide."""
    template = prs.slides[source_idx]
    slide_layout = template.slide_layout
    new_slide = prs.slides.add_slide(slide_layout)
    # Copy all shapes from template (we won't use this for complex duplication)
    return new_slide


def create_blank_dark_slide(prs):
    """Create a new blank slide with C_Title Only layout and dark bg."""
    layout = prs.slide_layouts[7]  # C_Title Only
    slide = prs.slides.add_slide(layout)
    set_slide_bg(slide, DARK_BG)
    return slide


# ── MAIN ──
INPUT  = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v1.1.pptx"
OUTPUT = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v2.0.pptx"

prs = Presentation(INPUT)

# We'll build the new deck by creating slides at end and then reordering.
# python-pptx doesn't support insert, so we add all new slides at end,
# then reorder the XML.


# ═══════════════════════════════════════════════════════════════
# EDIT EXISTING SLIDES
# ═══════════════════════════════════════════════════════════════

# --- Edit Slide 1 (Cover) - Add "Prepared for [Client Name]" + Date ---
slide1 = prs.slides[0]
add_textbox(slide1,
    left=Emu(609600), top=Emu(4800000), width=Emu(6000000), height=Emu(350000),
    text="Prepared for [Client Name]",
    font_size=SZ_SUBTITLE, bold=False, italic=True, color=LIGHT_BLUE,
    alignment=PP_ALIGN.LEFT)
add_textbox(slide1,
    left=Emu(609600), top=Emu(5150000), width=Emu(4000000), height=Emu(300000),
    text="March 2026  |  Confidential",
    font_size=SZ_TINY, bold=False, color=LIGHT_BLUE,
    alignment=PP_ALIGN.LEFT)

# --- Edit Slide 2 (Opportunity) - Add global stat ---
slide2 = prs.slides[1]
add_rounded_rect(slide2,
    left=Emu(8800000), top=Emu(1200000), width=Emu(3000000), height=Emu(1400000),
    fill_color=DARKER_CARD)
add_textbox(slide2,
    left=Emu(8900000), top=Emu(1250000), width=Emu(2800000), height=Emu(500000),
    text="$1.9T",
    font_size=SZ_BIG_STAT, bold=True, color=ORANGE,
    alignment=PP_ALIGN.CENTER)
add_multiline_textbox(slide2,
    left=Emu(8900000), top=Emu(1800000), width=Emu(2800000), height=Emu(600000),
    lines=[
        ("global automotive supply", SZ_SMALL, False, LIGHT_BLUE),
        ("chain market by 2027", SZ_SMALL, False, LIGHT_BLUE),
    ],
    alignment=PP_ALIGN.CENTER)

# --- Edit Slide 5 (Demand Forecasting, index 4) - Add before/after comparison ---
slide5 = prs.slides[4]
# Add a small "Before vs After" box at bottom-left area
add_rounded_rect(slide5,
    left=Emu(350000), top=Emu(5600000), width=Emu(5400000), height=Emu(850000),
    fill_color=DARKER_CARD)
add_textbox(slide5,
    left=Emu(450000), top=Emu(5620000), width=Emu(2500000), height=Emu(300000),
    text="Before (Excel)",
    font_size=SZ_TINY, bold=True, color=ORANGE,
    alignment=PP_ALIGN.CENTER)
add_textbox(slide5,
    left=Emu(3200000), top=Emu(5620000), width=Emu(2500000), height=Emu(300000),
    text="After (AI/ML)",
    font_size=SZ_TINY, bold=True, color=GREEN,
    alignment=PP_ALIGN.CENTER)
add_textbox(slide5,
    left=Emu(450000), top=Emu(5920000), width=Emu(2500000), height=Emu(500000),
    text="MAPE 35-50%  |  Monthly refresh\nNo confidence bands  |  Manual overrides",
    font_size=Emu(135000), bold=False, color=LIGHT_BLUE,
    alignment=PP_ALIGN.CENTER)
add_textbox(slide5,
    left=Emu(3200000), top=Emu(5920000), width=Emu(2500000), height=Emu(500000),
    text="MAPE 10-15%  |  Daily refresh\n95% confidence bands  |  Auto-trigger POs",
    font_size=Emu(135000), bold=False, color=NEAR_WHITE,
    alignment=PP_ALIGN.CENTER)

# --- Edit Slide 8 (Logistics, index 7) - Add consolidated savings bar ---
slide8 = prs.slides[7]
add_rounded_rect(slide8,
    left=Emu(350000), top=Emu(5850000), width=Emu(11500000), height=Emu(650000),
    fill_color=DARKER_CARD)
add_textbox(slide8,
    left=Emu(500000), top=Emu(5900000), width=Emu(3000000), height=Emu(500000),
    text="Total Logistics Impact",
    font_size=SZ_BODY, bold=True, color=AMBER,
    alignment=PP_ALIGN.LEFT)
# individual metrics
metrics = [
    ("12% fuel saved", MS_BLUE),
    ("85%+ OTD", GREEN),
    ("20% faster picks", ORANGE),
    ("18% lower WH cost", AMBER),
]
x_start = 4200000
for i, (txt, col) in enumerate(metrics):
    add_textbox(slide8,
        left=Emu(x_start + i * 2000000), top=Emu(5920000), width=Emu(1900000), height=Emu(400000),
        text=txt, font_size=SZ_TINY, bold=True, color=col,
        alignment=PP_ALIGN.CENTER)

# --- Edit Slide 9 (Agentic AI, index 8) - Add conversation examples ---
slide9 = prs.slides[8]
add_rounded_rect(slide9,
    left=Emu(6800000), top=Emu(3600000), width=Emu(5000000), height=Emu(2800000),
    fill_color=DARKER_CARD)
add_textbox(slide9,
    left=Emu(6900000), top=Emu(3650000), width=Emu(4800000), height=Emu(350000),
    text="Sample Conversations",
    font_size=SZ_BODY, bold=True, color=CYAN_ACCENT,
    alignment=PP_ALIGN.LEFT)

conversations = [
    ('\u2709 User: "Show me top 5 SKUs at stockout risk in Mumbai"', NEAR_WHITE),
    ('\u2192 Agent: Querying inventory model... 3 critical, 2 warning.', LIGHT_BLUE),
    ('   Auto-creating transfer request from Pune depot.', LIGHT_BLUE),
    ('', LIGHT_BLUE),
    ('\u2709 User: "What happens if port delays extend 2 weeks?"', NEAR_WHITE),
    ('\u2192 Agent: Running scenario... 12 SKUs impacted. Alt vendors', LIGHT_BLUE),
    ('   identified. Shall I raise emergency POs?', LIGHT_BLUE),
]
add_multiline_textbox(slide9,
    left=Emu(6900000), top=Emu(4050000), width=Emu(4800000), height=Emu(2300000),
    lines=[(txt, Emu(135000), False, col) for txt, col in conversations],
    alignment=PP_ALIGN.LEFT)


# ═══════════════════════════════════════════════════════════════
# ADD NEW SLIDES (appended at end, reordered later)
# ═══════════════════════════════════════════════════════════════

# ── NEW SLIDE A: Agenda (will be inserted after slide 1) ──
agenda_slide = create_blank_dark_slide(prs)
add_textbox(agenda_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Agenda",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(agenda_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="What we will cover today",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

agenda_items = [
    ("01", "The SAP Supply Chain Opportunity", "Why Toyota Australia should act now", MS_BLUE),
    ("02", "Toyota AU — Supply Chain Challenges", "Real pain points across 275 dealerships", CYAN_ACCENT),
    ("03", "Our Approach & Architecture", "Three-layer intelligence: Data → AI → Action", GREEN),
    ("04", "Four AI Use Cases", "Demand · Inventory · Supply Planning · Logistics", AMBER),
    ("05", "The Agentic AI Differentiator", "Copilot orchestrating all domains", ORANGE),
    ("06", "Why NTT DATA Business Solutions?", "SAP + AI + Automotive domain expertise", CYAN_ACCENT),
    ("07", "ROI & Business Case", "Consolidated impact across all use cases", MS_BLUE),
    ("08", "Implementation Roadmap", "12-week phased delivery plan", GREEN),
    ("09", "Next Steps", "Discovery workshop & POC proposal", AMBER),
]

y_base = 1500000
for i, (num, title, desc, col) in enumerate(agenda_items):
    y = y_base + i * 620000
    add_circle(agenda_slide, left=Emu(700000), top=Emu(y + 50000), size=Emu(430000), fill_color=col)
    add_textbox(agenda_slide,
        left=Emu(700000), top=Emu(y + 100000), width=Emu(430000), height=Emu(350000),
        text=num, font_size=SZ_SMALL, bold=True, color=WHITE,
        alignment=PP_ALIGN.CENTER)
    add_textbox(agenda_slide,
        left=Emu(1300000), top=Emu(y + 30000), width=Emu(5000000), height=Emu(350000),
        text=title, font_size=SZ_BODY, bold=True, color=WHITE)
    add_textbox(agenda_slide,
        left=Emu(1300000), top=Emu(y + 320000), width=Emu(5000000), height=Emu(300000),
        text=desc, font_size=SZ_TINY, bold=False, color=LIGHT_BLUE)
    # Right-side line decoration
    add_rounded_rect(agenda_slide,
        left=Emu(6800000), top=Emu(y + 120000), width=Emu(4800000), height=Emu(3000),
        fill_color=col)


# ── NEW SLIDE B: Industry Context — Toyota Australia Challenges ──
industry_slide = create_blank_dark_slide(prs)
add_textbox(industry_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Toyota Australia — Supply Chain Challenges",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(industry_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="Real challenges across your 275 dealerships that AI can solve today",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

trends = [
    ("Demand Volatility",
     "RAV4 sales down 74% in early\n"
     "2026 due to model transition\n"
     "gaps. [1]\n\n"
     "3–6 month wait times persist\n"
     "across the range. 200K+ unit\n"
     "target at risk without better\n"
     "demand visibility. [2]",
     MS_BLUE),
    ("Parts Forecasting\nGap",
     "No retail inventory management\n"
     "system across dealer network.\n"
     "[3]\n\n"
     "Cannot distinguish real demand\n"
     "from stock replenishment.\n"
     "Parts forecasting still relies\n"
     "on Excel and manual overrides.\n"
     "[3]",
     GREEN),
    ("Hybrid Supply\nCrunch",
     "Hybrid demand surged 3× in\n"
     "5 years — outstripping supply.\n"
     "[4]\n\n"
     "Aisin magnet & Denso inverter\n"
     "bottlenecks. All components\n"
     "shipped from Japan — logistics\n"
     "delays compound the problem.\n"
     "[4][5]",
     AMBER),
    ("Distribution\nComplexity",
     "275 dealers across 8 states.\n"
     "Vast geography from Darwin to\n"
     "Melbourne adds transit time.\n"
     "[6]\n\n"
     "Model transitions (Fortuner\n"
     "exit, new-gen RAV4 & HiLux)\n"
     "need dynamic stock rebalancing.\n"
     "[1]",
     ORANGE),
]

for i, (title, desc, col) in enumerate(trends):
    x = 400000 + i * 2900000
    add_rounded_rect(industry_slide,
        left=Emu(x), top=Emu(1500000), width=Emu(2700000), height=Emu(3200000),
        fill_color=DARK_CARD)
    # Color accent bar at top of card
    add_rounded_rect(industry_slide,
        left=Emu(x), top=Emu(1500000), width=Emu(2700000), height=Emu(60000),
        fill_color=col)
    add_textbox(industry_slide,
        left=Emu(x + 150000), top=Emu(1650000), width=Emu(2400000), height=Emu(500000),
        text=title, font_size=SZ_BODY, bold=True, color=col)
    add_multiline_textbox(industry_slide,
        left=Emu(x + 150000), top=Emu(2250000), width=Emu(2400000), height=Emu(2250000),
        lines=[(line, SZ_TINY, False, LIGHT_BLUE) for line in desc.split('\n')],
        alignment=PP_ALIGN.LEFT)

# Bottom insight bar
add_rounded_rect(industry_slide,
    left=Emu(400000), top=Emu(4900000), width=Emu(11400000), height=Emu(600000),
    fill_color=DARKER_CARD)
add_textbox(industry_slide,
    left=Emu(600000), top=Emu(4930000), width=Emu(1800000), height=Emu(350000),
    text="Key Insight:",
    font_size=SZ_BODY, bold=True, color=CYAN_ACCENT)
add_textbox(industry_slide,
    left=Emu(2500000), top=Emu(4930000), width=Emu(9000000), height=Emu(500000),
    text="Toyota AU's SAP ECC6 holds years of order, parts and logistics data — but no AI layer to predict, optimise and act autonomously. This is exactly what NDBS delivers.",
    font_size=SZ_SMALL, bold=False, color=NEAR_WHITE)

# Sources footer
SZ_REF = Pt(7)
source_lines = [
    "[1] CarsGuide — Toyota wait times & RAV4 sales 2026",
    "[2] CarsGuide — Toyota wait times in Australia 2025",
    "[3] Automotive Logistics — Toyota 'holy grail' of predictability",
    "[4] CBT News — Toyota struggles to meet surging hybrid demand",
    "[5] FreightAmigo — Toyota recovery from chip shortages case study",
    "[6] Toyota Australia — Dealer network & corporate overview",
]
add_textbox(industry_slide,
    left=Emu(400000), top=Emu(5550000), width=Emu(5500000), height=Emu(200000),
    text="Sources:",
    font_size=SZ_REF, bold=True, color=LIGHT_BLUE)
add_multiline_textbox(industry_slide,
    left=Emu(400000), top=Emu(5700000), width=Emu(11400000), height=Emu(1000000),
    lines=[(line, SZ_REF, False, RGBColor(0x88, 0x99, 0xAA)) for line in source_lines],
    alignment=PP_ALIGN.LEFT)


# ── NEW SLIDE C: Technology Stack Architecture (after Data Integration) ──
tech_slide = create_blank_dark_slide(prs)
add_textbox(tech_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="End-to-End Technology Architecture",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(tech_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="From SAP source systems to autonomous AI actions — all on Microsoft Azure",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

# Architecture flow — 5 boxes with arrows
arch_boxes = [
    ("SAP Systems", "ECC / S4HANA\nBW / APO\nMM · SD · PP · TM", MS_BLUE),
    ("Ingestion", "Azure Data Factory\nSAP ODP / BAPI\nCDC via SLT", CYAN_ACCENT),
    ("Data Platform", "Microsoft Fabric\nBronze → Silver → Gold\nDelta Lakehouse", GREEN),
    ("AI / ML Engine", "Azure ML Studio\nProphet · LightGBM\nOR-Tools · OpenAI", AMBER),
    ("Action Layer", "Copilot Studio\nAgentic AI Bots\nSAP Back-Write", ORANGE),
]

box_w = 2000000
box_h = 2200000
gap = 200000
total_w = len(arch_boxes) * box_w + (len(arch_boxes) - 1) * gap
x_start = (SLIDE_W - total_w) // 2

for i, (title, desc, col) in enumerate(arch_boxes):
    x = x_start + i * (box_w + gap)
    y = 1600000
    add_rounded_rect(tech_slide,
        left=Emu(x), top=Emu(y), width=Emu(box_w), height=Emu(box_h),
        fill_color=DARK_CARD)
    # Top accent bar
    add_rounded_rect(tech_slide,
        left=Emu(x), top=Emu(y), width=Emu(box_w), height=Emu(60000),
        fill_color=col)
    # Step number
    add_textbox(tech_slide,
        left=Emu(x + 100000), top=Emu(y + 150000), width=Emu(box_w - 200000), height=Emu(400000),
        text=f"0{i+1}", font_size=SZ_NUMBER, bold=True, color=col,
        alignment=PP_ALIGN.CENTER)
    # Title
    add_textbox(tech_slide,
        left=Emu(x + 100000), top=Emu(y + 550000), width=Emu(box_w - 200000), height=Emu(350000),
        text=title, font_size=SZ_BODY, bold=True, color=WHITE,
        alignment=PP_ALIGN.CENTER)
    # Description
    add_multiline_textbox(tech_slide,
        left=Emu(x + 100000), top=Emu(y + 950000), width=Emu(box_w - 200000), height=Emu(1200000),
        lines=[(line, SZ_TINY, False, LIGHT_BLUE) for line in desc.split('\n')],
        alignment=PP_ALIGN.CENTER)
    # Arrow between boxes
    if i < len(arch_boxes) - 1:
        arrow_x = x + box_w + 10000
        add_chevron_arrow(tech_slide,
            left=Emu(arrow_x), top=Emu(y + 900000), width=Emu(180000), height=Emu(350000),
            fill_color=col)

# Bottom bar — governance
add_rounded_rect(tech_slide,
    left=Emu(x_start), top=Emu(4200000), width=Emu(total_w), height=Emu(550000),
    fill_color=DARKER_CARD)
add_textbox(tech_slide,
    left=Emu(x_start + 200000), top=Emu(4250000), width=Emu(total_w - 400000), height=Emu(250000),
    text="Governance & Security Layer",
    font_size=SZ_BODY, bold=True, color=CYAN_ACCENT,
    alignment=PP_ALIGN.CENTER)
add_textbox(tech_slide,
    left=Emu(x_start + 200000), top=Emu(4500000), width=Emu(total_w - 400000), height=Emu(250000),
    text="Microsoft Purview  ·  Azure AD / Entra ID  ·  RBAC  ·  Data Lineage  ·  Encryption at Rest & Transit",
    font_size=SZ_TINY, bold=False, color=LIGHT_BLUE,
    alignment=PP_ALIGN.CENTER)


# ── NEW SLIDE D2: Why NTT DATA Business Solutions? ──
why_slide = create_blank_dark_slide(prs)
add_textbox(why_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Why NTT DATA Business Solutions?",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(why_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="The only partner that connects your SAP data to autonomous AI action",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

why_cards = [
    ("SAP-Native\nExpertise",
     "Your Challenge",
     "SAP ECC6 data is locked\ninside legacy modules.",
     "What We Bring",
     "20+ years delivering SAP for\nautomotive OEMs. Pre-built\nODP/BAPI connectors for\nMM, SD, PP, QM — no\ncustom ABAP required.",
     MS_BLUE),
    ("Microsoft AI\nPlatform",
     "Your Challenge",
     "No analytics layer on top\nof SAP transactional data.",
     "What We Bring",
     "Microsoft Fabric + Azure AI\nFoundry. Medallion architecture\n(Bronze → Gold) with built-in\ngovernance. Copilot Studio\nfor natural-language access.",
     GREEN),
    ("Automotive\nDomain IP",
     "Your Challenge",
     "Generic AI tools don't\nunderstand auto supply chains.",
     "What We Bring",
     "Pre-trained models for parts\ndemand, dealer ordering\npatterns & logistics across\nAU geography. Calibrated on\nautomotive-specific KPIs.",
     AMBER),
    ("Rapid Time\nto Value",
     "Your Challenge",
     "Can't wait 12+ months for\na traditional BI programme.",
     "What We Bring",
     "12-week delivery: first value\nat Week 6. Proven accelerators\nfor SAP-to-Fabric ingestion.\nPOC in 6 weeks with live\nToyota AU data.",
     ORANGE),
]

for i, (title, challenge_hdr, challenge, bring_hdr, bring, col) in enumerate(why_cards):
    x = 400000 + i * 2900000
    card_top = 1400000
    card_h = 4200000
    add_rounded_rect(why_slide,
        left=Emu(x), top=Emu(card_top), width=Emu(2700000), height=Emu(card_h),
        fill_color=DARK_CARD)
    # Accent bar
    add_rounded_rect(why_slide,
        left=Emu(x), top=Emu(card_top), width=Emu(2700000), height=Emu(60000),
        fill_color=col)
    # Card title
    add_textbox(why_slide,
        left=Emu(x + 150000), top=Emu(card_top + 120000), width=Emu(2400000), height=Emu(500000),
        text=title, font_size=SZ_BODY, bold=True, color=col)
    # "Your Challenge" header
    add_textbox(why_slide,
        left=Emu(x + 150000), top=Emu(card_top + 650000), width=Emu(2400000), height=Emu(250000),
        text=challenge_hdr, font_size=SZ_TINY, bold=True, color=AMBER)
    # Challenge text
    add_multiline_textbox(why_slide,
        left=Emu(x + 150000), top=Emu(card_top + 900000), width=Emu(2400000), height=Emu(600000),
        lines=[(line, SZ_TINY, False, NEAR_WHITE) for line in challenge.split('\n')],
        alignment=PP_ALIGN.LEFT)
    # "What We Bring" header
    add_textbox(why_slide,
        left=Emu(x + 150000), top=Emu(card_top + 1550000), width=Emu(2400000), height=Emu(250000),
        text=bring_hdr, font_size=SZ_TINY, bold=True, color=GREEN)
    # Bring text
    add_multiline_textbox(why_slide,
        left=Emu(x + 150000), top=Emu(card_top + 1800000), width=Emu(2400000), height=Emu(2200000),
        lines=[(line, SZ_TINY, False, LIGHT_BLUE) for line in bring.split('\n')],
        alignment=PP_ALIGN.LEFT)


# ── NEW SLIDE D: Consolidated ROI (after Agentic AI slide) ──
roi_slide = create_blank_dark_slide(prs)
add_textbox(roi_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Consolidated ROI & Business Case",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(roi_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="Combined impact across all four AI use cases",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

# Big ROI stats row
roi_stats = [
    ("3.2×", "Overall ROI\nvs. manual planning", MS_BLUE),
    ("₹15-25Cr", "Annual savings\nacross supply chain", AMBER),
    ("30-40%", "Forecast error\nreduction (MAPE)", GREEN),
    ("85%+", "On-time delivery\nachievement", ORANGE),
]
stat_w = 2600000
stat_gap = 200000
stat_total = len(roi_stats) * stat_w + (len(roi_stats) - 1) * stat_gap
stat_x0 = (SLIDE_W - stat_total) // 2

for i, (val, desc, col) in enumerate(roi_stats):
    x = stat_x0 + i * (stat_w + stat_gap)
    add_rounded_rect(roi_slide,
        left=Emu(x), top=Emu(1500000), width=Emu(stat_w), height=Emu(1600000),
        fill_color=DARK_CARD)
    add_textbox(roi_slide,
        left=Emu(x), top=Emu(1600000), width=Emu(stat_w), height=Emu(600000),
        text=val, font_size=SZ_BIG_STAT, bold=True, color=col,
        alignment=PP_ALIGN.CENTER)
    add_multiline_textbox(roi_slide,
        left=Emu(x + 100000), top=Emu(2250000), width=Emu(stat_w - 200000), height=Emu(700000),
        lines=[(line, SZ_SMALL, False, LIGHT_BLUE) for line in desc.split('\n')],
        alignment=PP_ALIGN.CENTER)

# Use case breakdown table
uc_data = [
    ("Demand Forecasting", "30-40% ↓ forecast error", "₹2-5Cr freed/plant", "8 weeks"),
    ("Inventory Optimisation", "25% ↓ excess stock", "₹3-8Cr saved", "6 weeks"),
    ("Supply Planning", "40% faster S&OP cycle", "₹2-4Cr risk avoided", "8 weeks"),
    ("Logistics Optimisation", "12% ↓ transport cost", "₹5-8Cr logistics saved", "10 weeks"),
]

table_y = 3500000
headers = ["Use Case", "Key Metric", "Financial Impact", "Time to Value"]
add_rounded_rect(roi_slide,
    left=Emu(400000), top=Emu(table_y), width=Emu(11400000), height=Emu(2200000),
    fill_color=DARK_CARD)

# Header row
for j, hdr in enumerate(headers):
    add_textbox(roi_slide,
        left=Emu(500000 + j * 2850000), top=Emu(table_y + 100000), width=Emu(2700000), height=Emu(350000),
        text=hdr, font_size=SZ_SMALL, bold=True, color=CYAN_ACCENT,
        alignment=PP_ALIGN.LEFT)

# Separator line
add_rounded_rect(roi_slide,
    left=Emu(500000), top=Emu(table_y + 450000), width=Emu(11100000), height=Emu(3000),
    fill_color=CYAN_ACCENT)

# Data rows
uc_colors = [MS_BLUE, AMBER, GREEN, ORANGE]
for i, (uc, metric, impact, ttv) in enumerate(uc_data):
    row_y = table_y + 550000 + i * 400000
    row_data = [uc, metric, impact, ttv]
    for j, cell in enumerate(row_data):
        col = uc_colors[i] if j == 0 else LIGHT_BLUE
        bld = True if j == 0 else False
        add_textbox(roi_slide,
            left=Emu(500000 + j * 2850000), top=Emu(row_y), width=Emu(2700000), height=Emu(350000),
            text=cell, font_size=SZ_TINY, bold=bld, color=col,
            alignment=PP_ALIGN.LEFT)


# ── NEW SLIDE E: Implementation Roadmap ──
roadmap_slide = create_blank_dark_slide(prs)
add_textbox(roadmap_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Implementation Roadmap",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(roadmap_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="12-week phased delivery — fast time to first value",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

phases = [
    ("Phase 1", "Weeks 1–4", "Data Foundation", [
        "SAP connector setup (ODP/BAPI)",
        "Fabric Lakehouse provisioning",
        "Bronze/Silver/Gold zone build",
        "Data quality & governance setup",
    ], MS_BLUE),
    ("Phase 2", "Weeks 5–8", "AI Models & Analytics", [
        "Demand forecasting model training",
        "Inventory optimization engine",
        "Supply planning algorithms",
        "Power BI semantic models",
    ], GREEN),
    ("Phase 3", "Weeks 9–12", "Agentic AI & Go-Live", [
        "Copilot Studio bot deployment",
        "Agent orchestration layer",
        "SAP back-write integration",
        "UAT, training & go-live",
    ], AMBER),
]

phase_w = 3500000
phase_gap = 300000
phase_total = len(phases) * phase_w + (len(phases) - 1) * phase_gap
phase_x0 = (SLIDE_W - phase_total) // 2

for i, (name, weeks, title, items, col) in enumerate(phases):
    x = phase_x0 + i * (phase_w + phase_gap)
    y = 1500000
    h = 4000000
    add_rounded_rect(roadmap_slide,
        left=Emu(x), top=Emu(y), width=Emu(phase_w), height=Emu(h),
        fill_color=DARK_CARD)
    # Top accent
    add_rounded_rect(roadmap_slide,
        left=Emu(x), top=Emu(y), width=Emu(phase_w), height=Emu(60000),
        fill_color=col)
    # Phase label
    add_textbox(roadmap_slide,
        left=Emu(x + 150000), top=Emu(y + 150000), width=Emu(phase_w - 300000), height=Emu(350000),
        text=f"{name}  |  {weeks}", font_size=SZ_SMALL, bold=True, color=col,
        alignment=PP_ALIGN.LEFT)
    # Phase title
    add_textbox(roadmap_slide,
        left=Emu(x + 150000), top=Emu(y + 500000), width=Emu(phase_w - 300000), height=Emu(400000),
        text=title, font_size=SZ_BODY, bold=True, color=WHITE,
        alignment=PP_ALIGN.LEFT)
    # Items
    items_text = '\n'.join([f"  {item}" for item in items])
    add_multiline_textbox(roadmap_slide,
        left=Emu(x + 150000), top=Emu(y + 1000000), width=Emu(phase_w - 300000), height=Emu(2800000),
        lines=[(f"  {item}", SZ_TINY, False, LIGHT_BLUE) for item in items],
        alignment=PP_ALIGN.LEFT)
    # Arrow between phases
    if i < len(phases) - 1:
        arrow_x = x + phase_w + 30000
        add_chevron_arrow(roadmap_slide,
            left=Emu(arrow_x), top=Emu(y + 1500000), width=Emu(240000), height=Emu(500000),
            fill_color=col)

# Bottom bar
add_rounded_rect(roadmap_slide,
    left=Emu(phase_x0), top=Emu(5800000), width=Emu(phase_total), height=Emu(550000),
    fill_color=DARKER_CARD)
add_textbox(roadmap_slide,
    left=Emu(phase_x0 + 200000), top=Emu(5850000), width=Emu(phase_total - 400000), height=Emu(450000),
    text="First value visible in Week 6 (demand forecast MVP)  ·  Full production by Week 12  ·  Ongoing optimization post go-live",
    font_size=SZ_TINY, bold=False, color=NEAR_WHITE,
    alignment=PP_ALIGN.CENTER)


# ── NEW SLIDE F: Next Steps & CTA (replaces empty slide 10) ──
nextsteps_slide = create_blank_dark_slide(prs)
add_textbox(nextsteps_slide,
    left=Emu(609600), top=Emu(300000), width=Emu(10000000), height=Emu(600000),
    text="Next Steps",
    font_size=SZ_TITLE, bold=True, color=WHITE)
add_textbox(nextsteps_slide,
    left=Emu(609600), top=Emu(850000), width=Emu(10000000), height=Emu(350000),
    text="How we move from presentation to production",
    font_size=SZ_SUBTITLE, bold=False, color=LIGHT_BLUE)

steps = [
    ("01", "Discovery Workshop", "2-day workshop to map your SAP landscape,\nprioritise use cases, and define success metrics.\nIncludes stakeholder interviews & data audit.", "Week 1-2", MS_BLUE),
    ("02", "POC Scope & Agreement", "Define POC boundaries — typically 1 use case\n(Demand Forecasting recommended as highest ROI).\nFixed-price, 6-week delivery.", "Week 3", GREEN),
    ("03", "POC Delivery", "End-to-end working prototype: SAP data → Fabric\n→ AI model → Copilot bot. With live SAP data,\nnot synthetic. Measurable accuracy baseline.", "Weeks 4-9", AMBER),
    ("04", "Scale & Productionise", "Expand to remaining use cases. Full security,\ngovernance, and operational readiness.\nHandover with training & runbooks.", "Weeks 10-16", ORANGE),
]

step_w = 2600000
step_gap = 200000
step_total = len(steps) * step_w + (len(steps) - 1) * step_gap
step_x0 = (SLIDE_W - step_total) // 2

for i, (num, title, desc, timeline, col) in enumerate(steps):
    x = step_x0 + i * (step_w + step_gap)
    y = 1500000
    add_rounded_rect(nextsteps_slide,
        left=Emu(x), top=Emu(y), width=Emu(step_w), height=Emu(3800000),
        fill_color=DARK_CARD)
    # Top accent
    add_rounded_rect(nextsteps_slide,
        left=Emu(x), top=Emu(y), width=Emu(step_w), height=Emu(60000),
        fill_color=col)
    # Number
    add_circle(nextsteps_slide,
        left=Emu(x + step_w // 2 - 250000), top=Emu(y + 200000), size=Emu(500000), fill_color=col)
    add_textbox(nextsteps_slide,
        left=Emu(x + step_w // 2 - 250000), top=Emu(y + 260000), width=Emu(500000), height=Emu(400000),
        text=num, font_size=SZ_BODY, bold=True, color=WHITE,
        alignment=PP_ALIGN.CENTER)
    # Title
    add_textbox(nextsteps_slide,
        left=Emu(x + 100000), top=Emu(y + 800000), width=Emu(step_w - 200000), height=Emu(400000),
        text=title, font_size=SZ_BODY, bold=True, color=WHITE,
        alignment=PP_ALIGN.CENTER)
    # Timeline badge
    add_textbox(nextsteps_slide,
        left=Emu(x + 100000), top=Emu(y + 1200000), width=Emu(step_w - 200000), height=Emu(300000),
        text=timeline, font_size=SZ_TINY, bold=True, color=col,
        alignment=PP_ALIGN.CENTER)
    # Description
    add_multiline_textbox(nextsteps_slide,
        left=Emu(x + 100000), top=Emu(y + 1600000), width=Emu(step_w - 200000), height=Emu(2000000),
        lines=[(line, SZ_TINY, False, LIGHT_BLUE) for line in desc.split('\n')],
        alignment=PP_ALIGN.LEFT)

# CTA bar at bottom
add_rounded_rect(nextsteps_slide,
    left=Emu(step_x0), top=Emu(5700000), width=Emu(step_total), height=Emu(700000),
    fill_color=MS_BLUE)
add_textbox(nextsteps_slide,
    left=Emu(step_x0 + 200000), top=Emu(5750000), width=Emu(step_total - 400000), height=Emu(300000),
    text="Ready to start?",
    font_size=SZ_BODY, bold=True, color=WHITE,
    alignment=PP_ALIGN.CENTER)
add_textbox(nextsteps_slide,
    left=Emu(step_x0 + 200000), top=Emu(6050000), width=Emu(step_total - 400000), height=Emu(300000),
    text="Contact us to schedule the Discovery Workshop  ·  [your.name@nttdata.com]  ·  [+91 XXXX XXXXXX]",
    font_size=SZ_SMALL, bold=False, color=NEAR_WHITE,
    alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════
# REORDER SLIDES
# ═══════════════════════════════════════════════════════════════
# Current order after additions (0-indexed):
#  0: Cover (edited)
#  1: Opportunity (edited)
#  2: Approach
#  3: Data Integration
#  4: Demand Forecasting (edited)
#  5: Inventory
#  6: Supply Planning
#  7: Logistics (edited)
#  8: Agentic AI (edited)
#  9: Old Closing (empty — to be replaced)
# 10: Copyright
# 11: Agenda (NEW)
# 12: Industry Context (NEW)
# 13: Tech Stack (NEW)
# 14: ROI (NEW)
# 15: Roadmap (NEW)
# 16: Next Steps (NEW)
# 17: Why NTT (NEW)

# Desired order:
#  0: Cover
#  1: Agenda (11)
#  2: Opportunity (1)
#  3: Industry Context (12)
#  4: Approach (2)
#  5: Data Integration (3)
#  6: Tech Stack (13)
#  7: Demand Forecasting (4)
#  8: Inventory (5)
#  9: Supply Planning (6)
# 10: Logistics (7)
# 11: Agentic AI (8)
# 12: Why NTT (17)
# 13: ROI (14)
# 14: Roadmap (15)
# 15: Next Steps (16)
# 16: Copyright (10)
# 17: Old empty closing (9) — kept to avoid duplicate XML name collision

desired_order = [0, 11, 1, 12, 2, 3, 13, 4, 5, 6, 7, 8, 14, 15, 16, 17, 10, 9]

# Reorder by manipulating the XML slide list
pres_elem = prs.part._element
ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
sldIdLst = pres_elem.find('.//p:sldIdLst', ns)
sldId_elements = list(sldIdLst)

# Build new order
new_order_elems = [sldId_elements[i] for i in desired_order]

# Clear and re-add in new order
for elem in sldId_elements:
    sldIdLst.remove(elem)

for elem in new_order_elems:
    sldIdLst.append(elem)

# ── Save ──
prs.save(OUTPUT)
print(f"Saved enhanced presentation to {OUTPUT}")
print(f"Total slides: {len(desired_order)}")
