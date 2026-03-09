"""
Re-do: Remove extra LIVE DEMO badges from non-use-case slides,
and add the missing ones. Target slides: Demand Forecasting (has '01' + 'Demand'),
Inventory (has '02' + 'Inventory'), Supply Planning (has '03' + 'Supply'),
Logistics (has '04' + 'Logistics').
"""

from pptx import Presentation
from pptx.util import Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

AMBER   = RGBColor(0xFF, 0xB9, 0x00)
DARK_BG = RGBColor(0x0A, 0x16, 0x28)

# Regenerate from v1.1 → apply all 3 scripts in sequence
from subprocess import run
import sys

# Start fresh from the enhance script
print("Step 1: Regenerating v2.0 from v1.1...")
run([sys.executable, "scripts/enhance_pptx.py"], check=True)

print("\nStep 2: Applying Toyota AU customisation...")
run([sys.executable, "scripts/toyota_au_customise.py"], check=True)

print("\nStep 3: Applying text fixes...")
run([sys.executable, "scripts/toyota_au_fixes.py"], check=True)

print("\nStep 4: Adding LIVE DEMO badges to correct slides only...")

INPUT  = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v2.0.pptx"
OUTPUT = "backend/generated_ppts/NDBS_SAP_Supply_Chain_AI_v2.0.pptx"
prs = Presentation(INPUT)

# Identify use case slides by title text
uc_titles = {
    "Demand Forecasting": None,
    "Inventory Optimisation": None,
    "Supply Planning": None,
    "Logistics Optimisation": None,
}

for idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if not hasattr(shape, 'text'):
            continue
        for uc_title in uc_titles:
            if uc_title in shape.text and uc_titles[uc_title] is None:
                # Check this is the main title (large font)
                if shape.has_text_frame:
                    for run in shape.text_frame.paragraphs[0].runs:
                        if run.font.size and run.font.size >= 400000:
                            uc_titles[uc_title] = idx
                            break

print("  Use case slides found:")
for title, idx in uc_titles.items():
    print(f"    {title}: slide {idx+1 if idx is not None else 'NOT FOUND'}")

# Add LIVE DEMO badges
for title, idx in uc_titles.items():
    if idx is None:
        continue
    slide = prs.slides[idx]
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Emu(10200000), Emu(350000), Emu(1700000), Emu(450000))
    badge.fill.solid()
    badge.fill.fore_color.rgb = AMBER
    badge.line.fill.background()
    tf = badge.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "LIVE DEMO"
    run.font.size = Emu(180000)
    run.font.bold = True
    run.font.color.rgb = DARK_BG
    print(f"  Added LIVE DEMO → slide {idx+1}: {title}")

prs.save(OUTPUT)
print(f"\nFinal v2.0 saved to {OUTPUT}")
