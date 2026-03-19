"""
Generate Seatrium SAP Pegasus Migration Briefing slides in NTT DATA blue theme.
16:9 format, 5-7 slides for internal team briefing.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# NTT DATA brand colors
NTT_BLUE = RGBColor(0x00, 0x32, 0x7A)       # Dark blue
NTT_LIGHT_BLUE = RGBColor(0x00, 0x7B, 0xC0) # Accent blue
NTT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
NTT_LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
NTT_DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
NTT_ACCENT = RGBColor(0x00, 0xA3, 0xE0)     # Bright accent blue

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def add_blue_bg(slide):
    """Add NTT DATA blue background to entire slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = NTT_BLUE


def add_white_bg(slide):
    """Add white background with blue header bar."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = NTT_WHITE


def add_header_bar(slide, title_text):
    """Add a blue header bar at top with title."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, Inches(1.2))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NTT_BLUE
    bar.line.fill.background()

    tf = bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.color.rgb = NTT_WHITE
    p.font.bold = True
    p.alignment = PP_ALIGN.LEFT
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.15)


def add_footer_bar(slide):
    """Add a thin blue footer bar with NTT DATA branding."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.0), SLIDE_W, Inches(0.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NTT_BLUE
    bar.line.fill.background()

    tf = bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NTT DATA  |  Confidential  |  Seatrium SAP Pegasus Migration"
    p.font.size = Pt(10)
    p.font.color.rgb = NTT_WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.margin_top = Inches(0.1)


def add_body_text(slide, left, top, width, height, text_items, font_size=16, bold_first=False):
    """Add a text box with bullet points."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(text_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = NTT_DARK_GRAY
        p.space_after = Pt(8)
        if bold_first and i == 0:
            p.font.bold = True
            p.font.color.rgb = NTT_BLUE
            p.font.size = Pt(font_size + 2)


def add_info_box(slide, left, top, width, height, title, items, box_color=None):
    """Add a colored info box with title and bullet items."""
    if box_color is None:
        box_color = NTT_LIGHT_GRAY

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    box.fill.solid()
    box.fill.fore_color.rgb = box_color
    box.line.color.rgb = NTT_LIGHT_BLUE
    box.line.width = Pt(1.5)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_right = Inches(0.2)

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NTT_BLUE
    p.space_after = Pt(6)

    for item in items:
        p = tf.add_paragraph()
        p.text = f"\u2022  {item}"
        p.font.size = Pt(13)
        p.font.color.rgb = NTT_DARK_GRAY
        p.space_after = Pt(4)


# ============================================================
# SLIDE 1: TITLE SLIDE
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
add_blue_bg(slide1)

# Accent line
line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.5), Inches(2), Inches(0.06))
line.fill.solid()
line.fill.fore_color.rgb = NTT_ACCENT
line.line.fill.background()

# Title
txBox = slide1.shapes.add_textbox(Inches(0.8), Inches(2.7), Inches(11), Inches(1.5))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Seatrium SAP Pegasus (OEP)"
p.font.size = Pt(40)
p.font.color.rgb = NTT_WHITE
p.font.bold = True

p2 = tf.add_paragraph()
p2.text = "Archival & Migration to Seatrium Cloud"
p2.font.size = Pt(36)
p2.font.color.rgb = NTT_ACCENT
p2.font.bold = True

# Subtitle
txBox2 = slide1.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(8), Inches(1))
tf2 = txBox2.text_frame
tf2.word_wrap = True
p3 = tf2.paragraphs[0]
p3.text = "Internal Team Briefing  |  NTT DATA"
p3.font.size = Pt(20)
p3.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)

p4 = tf2.add_paragraph()
p4.text = "March 2026  |  Confidential"
p4.font.size = Pt(16)
p4.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

# NTT DATA text branding bottom right
txBox3 = slide1.shapes.add_textbox(Inches(9.5), Inches(6.5), Inches(3.5), Inches(0.6))
tf3 = txBox3.text_frame
p5 = tf3.paragraphs[0]
p5.text = "NTT DATA"
p5.font.size = Pt(24)
p5.font.color.rgb = NTT_WHITE
p5.font.bold = True
p5.alignment = PP_ALIGN.RIGHT


# ============================================================
# SLIDE 2: CURRENT LANDSCAPE
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide2)
add_header_bar(slide2, "Current SAP Landscape at Seatrium")
add_footer_bar(slide2)

# SAP RISE box
add_info_box(slide2, 0.8, 1.6, 5.5, 2.5, "SAP RISE Environment", [
    "Pegasus (OEP) \u2013 Since 2021, contract ends Oct 2026",
    "Optimus (SEP) \u2013 Since 2021, migrated to S/4HANA 2025",
    "High Availability setup with multiple servers",
    "SAP App + S/4HANA DB + GRC (Access Control Mgmt)",
])

# Archive Center box
add_info_box(slide2, 7.0, 1.6, 5.5, 2.5, "OpenText Archive Center", [
    "Shared by both OEP & SEP systems",
    "Current size: 18TB \u2192 target 16TB by Aug 2026",
    "Linked to SAP for document archival",
    "Retention: Audit 5\u20137 years, SOT 10 years",
])

# Seatrium Cloud box
add_info_box(slide2, 0.8, 4.5, 5.5, 2.2, "Seatrium Cloud (Target)", [
    "Local cloud infrastructure managed by Seatrium",
    "Will host the migrated Pegasus (OEP) system",
    "Users access via Seatrium WAN",
    "Display access only \u2013 no transactional use",
])

# Key point
add_info_box(slide2, 7.0, 4.5, 5.5, 2.2, "Key Dates", [
    "SAP RISE contract: 2018 \u2013 Oct 2026",
    "Pegasus migration deadline: 30 Oct 2026",
    "Archive reduction target: 30 Aug 2026",
    "Current engagement started: 8 Aug 2024",
], box_color=RGBColor(0xE8, 0xF4, 0xFD))


# ============================================================
# SLIDE 3: CUSTOMER ASK / WHAT THEY WANT
# ============================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide3)
add_header_bar(slide3, "What Is the Customer Asking For?")
add_footer_bar(slide3)

requirements = [
    ("1.  Copy Pegasus Data", "All OEP data and attachments to be copied from SAP RISE to Seatrium Cloud"),
    ("2.  New SAP Server Setup", "New server in Seatrium Cloud with latest Windows version & service pack\n     hosting SAP Application, S/4HANA Database, and GRC module"),
    ("3.  Display-Only Access", "Users access via Seatrium WAN with display access only \u2013 no transactional processing"),
    ("4.  GRC Access Control", "GRC module to enable users to raise requests for display access"),
    ("5.  Auto User Termination", "Automatic termination of SAP user IDs based on Active Directory & Workday\n     using existing batch job processing"),
    ("6.  Archival Best Practices", "NTT DATA to propose best practice approach for data archival"),
    ("7.  OpenText Cleanup Support", "Support OpenText consultants in deleting SEP and OEP attachments\n     in both Seatrium Cloud and SAP RISE"),
]

y_pos = 1.5
for title, desc in requirements:
    # Title
    txBox = slide3.shapes.add_textbox(Inches(0.8), Inches(y_pos), Inches(11.5), Inches(0.35))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NTT_BLUE

    # Description
    txBox2 = slide3.shapes.add_textbox(Inches(1.2), Inches(y_pos + 0.32), Inches(11), Inches(0.45))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = desc
    p2.font.size = Pt(13)
    p2.font.color.rgb = NTT_DARK_GRAY
    p2.space_after = Pt(2)

    y_pos += 0.73


# ============================================================
# SLIDE 4: MIGRATION APPROACH (OPTION 1)
# ============================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide4)
add_header_bar(slide4, "Migration Approach \u2013 Option 1 (Proposed)")
add_footer_bar(slide4)

# FROM box
add_info_box(slide4, 0.8, 1.6, 5.5, 2.8, "FROM: SAP RISE", [
    "Pegasus (OEP) system \u2013 multiple HA servers",
    "SAP Application Server",
    "S/4HANA Database",
    "GRC (Access Control Management)",
    "OpenText Archive Center (shared OEP/SEP)",
    "Contract period: 2018 \u2013 Oct 2026",
])

# Arrow
arrow = slide4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.5), Inches(2.6), Inches(0.7), Inches(0.5))
arrow.fill.solid()
arrow.fill.fore_color.rgb = NTT_ACCENT
arrow.line.fill.background()

# TO box
add_info_box(slide4, 7.5, 1.6, 5.0, 2.8, "TO: Seatrium Cloud", [
    "Single server setup (App + DB + GRC)",
    "Latest Windows version & service pack",
    "Local copy of OEP attachments",
    "Display-only access via Seatrium WAN",
    "Auto user ID termination (AD + Workday)",
    "Cutover target: 30 Oct 2026",
], box_color=RGBColor(0xE8, 0xF4, 0xFD))

# Archive handling
add_info_box(slide4, 0.8, 4.8, 11.7, 1.8, "Archive Center Handling", [
    "Archive Center is shared between OEP (Pegasus) and SEP (Optimus) \u2013 careful separation needed",
    "Data reduction from 18TB to 16TB targeted by 30 Aug 2026",
    "NTT DATA to support OpenText consultants in deletion of SEP and OEP attachments",
    "Retention policies: Audit records 5\u20137 years, SOT records 10 years",
])


# ============================================================
# SLIDE 5: KEY CONSIDERATIONS & RISKS
# ============================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide5)
add_header_bar(slide5, "Key Considerations & Risks")
add_footer_bar(slide5)

add_info_box(slide5, 0.8, 1.6, 5.5, 2.5, "Technical Considerations", [
    "SAP RISE \u2192 on-prem migration (non-standard path)",
    "S/4HANA DB export/import or system copy approach",
    "GRC module configuration & role migration",
    "OpenText Archive Center data separation (OEP vs SEP)",
    "Network connectivity: Seatrium WAN for user access",
])

add_info_box(slide5, 7.0, 1.6, 5.5, 2.5, "Data & Compliance", [
    "18TB archive \u2192 16TB reduction before migration",
    "Audit retention: 5\u20137 years required",
    "SOT retention: 10 years required",
    "Display-only access \u2013 no data modification post-migration",
    "User ID lifecycle tied to AD & Workday",
])

add_info_box(slide5, 0.8, 4.5, 5.5, 2.2, "Timeline Risks", [
    "SAP RISE contract ends Oct 2026 \u2013 hard deadline",
    "Archive reduction must complete by Aug 2026",
    "OpenText consultant coordination dependency",
    "Server provisioning & OS patching lead times",
])

add_info_box(slide5, 7.0, 4.5, 5.5, 2.2, "Scope Clarity Needed", [
    "Single server vs HA \u2013 reduced from multi-server in RISE",
    "Exact scope of GRC module functionality to retain",
    "OpenText integration architecture in Seatrium Cloud",
    "Batch job migration for user ID auto-termination",
], box_color=RGBColor(0xFF, 0xF3, 0xE0))


# ============================================================
# SLIDE 6: NTT DATA SCOPE OF WORK
# ============================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide6)
add_header_bar(slide6, "NTT DATA \u2013 Scope of Work")
add_footer_bar(slide6)

workstreams = [
    ("SAP System Migration", "Export Pegasus from SAP RISE, provision new server in Seatrium Cloud,\nimport SAP App + S/4HANA DB + GRC, validate display-only access"),
    ("Archive Center", "Support OpenText consultants in data separation and deletion,\nensure local copy of attachments accessible from Seatrium Cloud"),
    ("Access Management", "Configure GRC for display-access request workflow,\nimplement auto-termination of user IDs via AD/Workday batch jobs"),
    ("Best Practices", "Propose archival best practices for SAP data retention,\nensure compliance with audit (5\u20137 yr) and SOT (10 yr) requirements"),
]

y_pos = 1.6
for i, (ws_title, ws_desc) in enumerate(workstreams):
    # Number circle
    circle = slide6.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), Inches(y_pos + 0.05), Inches(0.45), Inches(0.45))
    circle.fill.solid()
    circle.fill.fore_color.rgb = NTT_BLUE
    circle.line.fill.background()
    ctf = circle.text_frame
    ctf.paragraphs[0].text = str(i + 1)
    ctf.paragraphs[0].font.size = Pt(18)
    ctf.paragraphs[0].font.color.rgb = NTT_WHITE
    ctf.paragraphs[0].font.bold = True
    ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE

    # Title + Description
    txBox = slide6.shapes.add_textbox(Inches(1.5), Inches(y_pos), Inches(10.5), Inches(1.1))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = ws_title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NTT_BLUE

    p2 = tf.add_paragraph()
    p2.text = ws_desc
    p2.font.size = Pt(13)
    p2.font.color.rgb = NTT_DARK_GRAY
    p2.space_before = Pt(4)

    y_pos += 1.3


# ============================================================
# SLIDE 7: NEXT STEPS
# ============================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_white_bg(slide7)
add_header_bar(slide7, "Next Steps")
add_footer_bar(slide7)

add_info_box(slide7, 0.8, 1.6, 11.7, 2.5, "Immediate Actions", [
    "Confirm scope and detailed requirements with Seatrium team",
    "Assess current Pegasus system size (DB, application, attachments)",
    "Define target architecture for Seatrium Cloud (server specs, OS, network)",
    "Align with OpenText consultants on archive separation plan",
    "Establish project timeline working back from Oct 2026 deadline",
])

add_info_box(slide7, 0.8, 4.4, 5.5, 2.3, "Key Milestones", [
    "Aug 2026: Archive reduction 18TB \u2192 16TB",
    "Oct 2026: SAP RISE contract end / cutover",
    "Post-migration: Validate display access & GRC",
    "Ongoing: User ID auto-termination monitoring",
])

add_info_box(slide7, 7.0, 4.4, 5.5, 2.3, "NTT DATA Team Actions", [
    "Draft detailed migration plan & approach",
    "Prepare effort estimate & resource plan",
    "Schedule technical discovery workshop",
    "Identify archival best practice recommendations",
], box_color=RGBColor(0xE8, 0xF4, 0xFD))


# Save
output_path = "/home/user/ntt/docs/Seatrium_SAP_Pegasus_Migration_Briefing.pptx"
import os
os.makedirs("/home/user/ntt/docs", exist_ok=True)
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
