"""Toyota Australia — AI Use Case Presentation Generator.

Generates a comprehensive 16:9 PowerPoint deck covering AI use cases
for Toyota Motors Australia across S/4 HANA modules:
  - Demand Forecasting
  - Inventory Optimization
  - Supply Planning
  - Logistics Optimization
"""

import os
from datetime import datetime

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Brand Colors ─────────────────────────────────────────────
TOYOTA_RED = RGBColor(0xEB, 0x00, 0x23)
DARK_RED = RGBColor(0xC8, 0x00, 0x1E)
NAVY = RGBColor(0x1A, 0x1A, 0x2E)
DARK_BLUE = RGBColor(0x16, 0x21, 0x3E)
ACCENT_BLUE = RGBColor(0x00, 0x70, 0xF2)
SAP_GOLD = RGBColor(0xF0, 0xAB, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
MED_GRAY = RGBColor(0x88, 0x88, 0x88)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
GREEN = RGBColor(0x00, 0x96, 0x4B)
ORANGE = RGBColor(0xFF, 0x8C, 0x00)
TEAL = RGBColor(0x00, 0x89, 0x9B)

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "generated_ppts",
)


class ToyotaAIPPTGenerator:
    """Generates Toyota Australia AI use case presentation."""

    SLIDE_W = Inches(13.333)
    SLIDE_H = Inches(7.5)

    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Helpers ───────────────────────────────────────────────

    def _prs(self) -> Presentation:
        prs = Presentation()
        prs.slide_width = self.SLIDE_W
        prs.slide_height = self.SLIDE_H
        return prs

    def _add_text(self, slide, left, top, width, height, text,
                  size=14, bold=False, color=DARK_GRAY, align=PP_ALIGN.LEFT,
                  font="Calibri", wrap=True):
        tb = slide.shapes.add_textbox(left, top, width, height)
        tb.text_frame.word_wrap = wrap
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font
        p.alignment = align
        return tb

    def _add_bullets(self, slide, left, top, width, items, size=13,
                     color=DARK_GRAY, spacing=Inches(0.32)):
        cur = top
        for item in items:
            self._add_text(slide, left, cur, width, Inches(0.35),
                           f"\u2022  {item}", size=size, color=color)
            cur += spacing
        return cur

    def _bar(self, slide, color=NAVY):
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, self.SLIDE_W, Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()
        return bar

    def _slide_title(self, slide, text, color=NAVY):
        self._bar(slide, color)
        self._add_text(slide, Inches(0.75), Inches(0.18), Inches(11.5),
                       Inches(0.7), text, size=28, bold=True, color=WHITE)

    def _footer(self, slide, dark=False):
        self._add_text(
            slide, Inches(0.75), Inches(7.0), Inches(11.5), Inches(0.3),
            "Toyota Motors Australia  |  AI-Powered S/4 HANA Transformation  |  Confidential",
            size=9, color=WHITE if dark else MED_GRAY,
            align=PP_ALIGN.RIGHT,
        )

    def _box(self, slide, left, top, w, h, fill_color, text="",
             text_size=12, text_color=WHITE, bold=False, border_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                       left, top, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        if text:
            tf = shape.text_frame
            tf.word_wrap = True
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = Pt(text_size)
            p.font.bold = bold
            p.font.color.rgb = text_color
            p.font.name = "Calibri"
            tf.paragraphs[0].space_before = Pt(4)
        return shape

    def _arrow_right(self, slide, left, top, w=Inches(0.5), h=Inches(0.3)):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW, left, top, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = MED_GRAY
        shape.line.fill.background()
        return shape

    def _arrow_down(self, slide, left, top, w=Inches(0.3), h=Inches(0.4)):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.DOWN_ARROW, left, top, w, h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = MED_GRAY
        shape.line.fill.background()
        return shape

    def _section_divider(self, prs, section_num, title, subtitle):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = DARK_BLUE
        # Section number
        self._add_text(slide, Inches(1), Inches(2.2), Inches(11), Inches(0.8),
                       f"SECTION {section_num}", size=16, color=SAP_GOLD,
                       bold=True)
        # Accent line
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.0), Inches(2), Pt(3))
        line.fill.solid()
        line.fill.fore_color.rgb = TOYOTA_RED
        line.line.fill.background()
        # Title
        self._add_text(slide, Inches(1), Inches(3.3), Inches(11), Inches(1.2),
                       title, size=36, bold=True, color=WHITE)
        # Subtitle
        self._add_text(slide, Inches(1), Inches(4.5), Inches(11), Inches(0.8),
                       subtitle, size=18, color=SAP_GOLD)
        self._footer(slide, dark=True)

    # ── Slide Builders ────────────────────────────────────────

    def _slide_cover(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = NAVY

        # Red accent bar at top
        top_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, self.SLIDE_W, Inches(0.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = TOYOTA_RED
        top_bar.line.fill.background()

        # Gold line
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(1), Inches(2.5), Inches(2.5), Pt(3))
        line.fill.solid()
        line.fill.fore_color.rgb = SAP_GOLD
        line.line.fill.background()

        self._add_text(slide, Inches(1), Inches(2.8), Inches(11), Inches(1.5),
                       "AI-Powered Supply Chain Transformation",
                       size=40, bold=True, color=WHITE)
        self._add_text(slide, Inches(1), Inches(4.2), Inches(11), Inches(0.8),
                       "Toyota Motors Australia  |  S/4 HANA Integration",
                       size=22, color=SAP_GOLD)
        self._add_text(slide, Inches(1), Inches(5.2), Inches(11), Inches(0.5),
                       "Demand Forecasting  \u2022  Inventory Optimization  \u2022  Supply Planning  \u2022  Logistics Optimization",
                       size=14, color=WHITE)
        self._add_text(slide, Inches(1), Inches(6.2), Inches(11), Inches(0.4),
                       datetime.now().strftime("Prepared: %B %Y"),
                       size=12, color=MED_GRAY)
        self._footer(slide, dark=True)

    def _slide_agenda(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Agenda")

        items = [
            ("01", "Executive Summary", "Business context and strategic objectives"),
            ("02", "Current State — S/4 HANA Landscape", "Existing SAP modules and operational footprint"),
            ("03", "AI Use Cases Overview", "Four AI capabilities across the value chain"),
            ("04", "End-to-End Process Flow", "How AI integrates with S/4 HANA modules"),
            ("05", "Use Case Deep Dives", "Demand Forecasting, Inventory, Supply Planning, Logistics"),
            ("06", "Benefits & ROI", "Quantified business outcomes and KPIs"),
            ("07", "Challenges & Mitigations", "Implementation risks and mitigation strategies"),
            ("08", "Roadmap & Next Steps", "Phased implementation approach"),
        ]
        top = Inches(1.5)
        for num, title, desc in items:
            self._box(slide, Inches(0.75), top, Inches(0.8), Inches(0.55),
                      TOYOTA_RED, num, text_size=14, bold=True)
            self._add_text(slide, Inches(1.8), top + Inches(0.02),
                           Inches(4), Inches(0.3), title, size=15, bold=True,
                           color=NAVY)
            self._add_text(slide, Inches(1.8), top + Inches(0.28),
                           Inches(10), Inches(0.3), desc, size=11,
                           color=MED_GRAY)
            top += Inches(0.7)
        self._footer(slide)

    def _slide_exec_summary(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Executive Summary")

        self._add_text(
            slide, Inches(0.75), Inches(1.4), Inches(11.5), Inches(0.8),
            "Toyota Motors Australia operates one of the most complex automotive supply chains "
            "in the Asia-Pacific region, serving 280+ dealerships across the country. With S/4 HANA "
            "already underpinning procurement, inventory, warehouse management, and distribution, "
            "Toyota is uniquely positioned to layer AI capabilities that drive predictive, "
            "autonomous decision-making across the entire value chain.",
            size=14, color=DARK_GRAY,
        )

        # Four pillars
        cols = [
            ("Demand\nForecasting", "Predict dealership\ndemand for vehicles\nand parts", ACCENT_BLUE),
            ("Inventory\nOptimization", "Optimal stock levels\nacross warehouses\nand dealers", GREEN),
            ("Supply\nPlanning", "Adjust procurement\nand logistics based\non predictions", ORANGE),
            ("Logistics\nOptimization", "Move vehicles and\nparts efficiently\nacross network", TEAL),
        ]
        left = Inches(0.75)
        for title, desc, clr in cols:
            self._box(slide, left, Inches(2.6), Inches(2.8), Inches(0.6),
                      clr, title, text_size=14, bold=True)
            self._add_text(slide, left + Inches(0.15), Inches(3.35),
                           Inches(2.5), Inches(0.9), desc, size=11,
                           color=DARK_GRAY)
            left += Inches(3.05)

        # Key metrics
        self._add_text(slide, Inches(0.75), Inches(4.5), Inches(11), Inches(0.4),
                       "Expected Business Impact", size=16, bold=True, color=NAVY)
        metrics = [
            ("15-25%", "Reduction in\nexcess inventory"),
            ("20-30%", "Improvement in\nforecast accuracy"),
            ("10-15%", "Reduction in\nlogistics costs"),
            ("8-12%", "Improvement in\nservice levels"),
        ]
        left = Inches(0.75)
        for val, lbl in metrics:
            self._add_text(slide, left, Inches(5.0), Inches(2.5), Inches(0.5),
                           val, size=32, bold=True, color=TOYOTA_RED)
            self._add_text(slide, left, Inches(5.7), Inches(2.5), Inches(0.6),
                           lbl, size=12, color=MED_GRAY)
            left += Inches(3.05)
        self._footer(slide)

    def _slide_current_state(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Current State — S/4 HANA Landscape at Toyota Australia")

        modules = [
            ("S/4 HANA Procurement", "Direct Procurement",
             ["Vehicle component sourcing from OEM suppliers",
              "Parts & accessories procurement from tier-1/2 suppliers",
              "Purchase order management and vendor evaluation",
              "Contract management and pricing agreements"],
             ACCENT_BLUE),
            ("S/4 HANA Inventory", "Vehicles & Parts",
             ["Real-time inventory tracking across 280+ dealers",
              "Vehicle stock management (new, demo, pre-delivery)",
              "Parts inventory with min/max thresholds",
              "Batch and serial number tracking"],
             GREEN),
            ("Extended Warehouse Mgmt", "Parts & Accessories",
             ["Multi-warehouse operations (national + regional DCs)",
              "Pick/pack/ship for dealer orders",
              "Returns and quality inspection workflows",
              "Yard management for vehicle storage"],
             ORANGE),
            ("S/4 HANA Sales & Dist.", "Dealership Demand",
             ["Dealer order processing and allocation",
              "Demand-based distribution to dealerships",
              "Pricing, discounts, and incentive programs",
              "Delivery scheduling and transport planning"],
             TEAL),
        ]

        top = Inches(1.4)
        for title, scope, bullets, clr in modules:
            self._box(slide, Inches(0.75), top, Inches(3), Inches(0.5),
                      clr, f"{title} — {scope}", text_size=12, bold=True)
            bt = top + Inches(0.05)
            for b in bullets:
                self._add_text(slide, Inches(4.0), bt, Inches(8.5),
                               Inches(0.28), f"\u2022  {b}", size=11,
                               color=DARK_GRAY)
                bt += Inches(0.28)
            top += Inches(1.35)
        self._footer(slide)

    def _slide_process_flow_overview(self, prs):
        """End-to-end process flow: data sources → AI engine → S/4 HANA actions."""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "End-to-End AI Process Flow — Toyota Supply Chain")

        # Row 1: Data Sources
        self._add_text(slide, Inches(0.5), Inches(1.3), Inches(3), Inches(0.35),
                       "DATA SOURCES", size=12, bold=True, color=TOYOTA_RED)
        sources = [
            "S/4 HANA\nTransactional Data",
            "Dealer POS\n& Orders",
            "Market Data\n& Seasonality",
            "Logistics\nNetwork Data",
        ]
        left = Inches(0.5)
        for s in sources:
            self._box(slide, left, Inches(1.7), Inches(2.6), Inches(0.75),
                      LIGHT_GRAY, s, text_size=10, text_color=DARK_GRAY,
                      border_color=MED_GRAY)
            left += Inches(2.9)

        # Arrows down
        for i in range(4):
            self._arrow_down(slide, Inches(1.5 + i * 2.9), Inches(2.5))

        # Row 2: AI Processing Layer
        self._add_text(slide, Inches(0.5), Inches(2.95), Inches(3), Inches(0.35),
                       "AI PROCESSING LAYER", size=12, bold=True, color=TOYOTA_RED)
        ai_blocks = [
            ("Demand\nForecasting\nML Models", ACCENT_BLUE),
            ("Inventory\nOptimization\nAlgorithms", GREEN),
            ("Supply Planning\nOptimization\nEngine", ORANGE),
            ("Logistics Route\n& Load\nOptimization", TEAL),
        ]
        left = Inches(0.5)
        for txt, clr in ai_blocks:
            self._box(slide, left, Inches(3.35), Inches(2.6), Inches(0.85),
                      clr, txt, text_size=10, bold=True)
            left += Inches(2.9)

        # Arrows down
        for i in range(4):
            self._arrow_down(slide, Inches(1.5 + i * 2.9), Inches(4.25))

        # Row 3: S/4 HANA Actions
        self._add_text(slide, Inches(0.5), Inches(4.7), Inches(3), Inches(0.35),
                       "S/4 HANA AUTOMATED ACTIONS", size=12, bold=True,
                       color=TOYOTA_RED)
        actions = [
            "Auto-generate\nPurchase Orders\n(MM/Procurement)",
            "Reorder Point\nAdjustment\n(MM/Inventory)",
            "Warehouse Task\nPrioritization\n(EWM)",
            "Delivery Route\nOptimization\n(SD/TM)",
        ]
        left = Inches(0.5)
        for a in actions:
            self._box(slide, left, Inches(5.1), Inches(2.6), Inches(0.85),
                      NAVY, a, text_size=10, bold=True)
            left += Inches(2.9)

        # Feedback loop arrow text
        self._add_text(slide, Inches(0.5), Inches(6.15), Inches(12), Inches(0.35),
                       "\u21BB  Continuous feedback loop: Actual vs. Predicted outcomes feed back into ML models for self-improving accuracy",
                       size=11, color=TOYOTA_RED, bold=True)
        self._footer(slide)

    def _slide_detailed_flow(self, prs):
        """Detailed flow showing module interactions."""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Detailed Integration Flow — S/4 HANA Module Interactions")

        # Left column: The flow steps
        steps = [
            ("1", "Dealer places order / POS data captured", "SD Module", TEAL),
            ("2", "AI Demand Engine generates 30/60/90-day forecast", "AI Layer", ACCENT_BLUE),
            ("3", "Inventory Optimizer calculates optimal stock levels", "AI Layer", GREEN),
            ("4", "MRP run triggered with AI-adjusted parameters", "MM Module", NAVY),
            ("5", "Purchase requisitions auto-created for shortfalls", "Procurement", ACCENT_BLUE),
            ("6", "EWM receives inbound delivery & optimizes putaway", "EWM Module", ORANGE),
            ("7", "AI Logistics engine optimizes outbound routes", "AI Layer", TEAL),
            ("8", "SD creates delivery with optimized transport plan", "SD Module", TEAL),
        ]
        top = Inches(1.35)
        for num, desc, module, clr in steps:
            self._box(slide, Inches(0.5), top, Inches(0.5), Inches(0.45),
                      clr, num, text_size=14, bold=True)
            self._add_text(slide, Inches(1.15), top + Inches(0.03),
                           Inches(6.5), Inches(0.4), desc, size=12,
                           color=DARK_GRAY)
            self._box(slide, Inches(7.8), top, Inches(1.5), Inches(0.45),
                      clr, module, text_size=10, bold=True)
            top += Inches(0.58)

        # Right column: Module legend
        self._add_text(slide, Inches(9.8), Inches(1.35), Inches(3), Inches(0.35),
                       "S/4 HANA Modules", size=14, bold=True, color=NAVY)
        legend = [
            ("SD", "Sales & Distribution", TEAL),
            ("MM", "Materials Management", NAVY),
            ("EWM", "Extended Warehouse Mgmt", ORANGE),
            ("AI", "AI Processing Layer", ACCENT_BLUE),
        ]
        lt = Inches(1.85)
        for code, name, clr in legend:
            self._box(slide, Inches(9.8), lt, Inches(0.6), Inches(0.35),
                      clr, code, text_size=10, bold=True)
            self._add_text(slide, Inches(10.5), lt + Inches(0.02),
                           Inches(2.5), Inches(0.3), name, size=11,
                           color=DARK_GRAY)
            lt += Inches(0.45)

        # Data flow note
        self._add_text(slide, Inches(9.8), Inches(3.8), Inches(3), Inches(2.5),
                       "Key Integration Points:\n\n"
                       "\u2022 BAPIs for real-time data extraction\n"
                       "\u2022 SAP BTP for AI model hosting\n"
                       "\u2022 CPI for event-driven messaging\n"
                       "\u2022 Fiori apps for user dashboards\n"
                       "\u2022 SAP Analytics Cloud for reporting",
                       size=11, color=DARK_GRAY)
        self._footer(slide)

    def _slide_use_case(self, prs, title, subtitle, description,
                        how_it_works, sap_integration, kpis, color):
        """Deep-dive slide for each AI use case."""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, title, color)

        # Description
        self._add_text(slide, Inches(0.75), Inches(1.3), Inches(11.5),
                       Inches(0.5), subtitle, size=16, bold=True, color=color)
        self._add_text(slide, Inches(0.75), Inches(1.8), Inches(11.5),
                       Inches(0.6), description, size=13, color=DARK_GRAY)

        # Two columns
        # Left: How it Works
        self._add_text(slide, Inches(0.75), Inches(2.6), Inches(5.5),
                       Inches(0.35), "How It Works", size=14, bold=True,
                       color=NAVY)
        self._add_bullets(slide, Inches(0.75), Inches(3.0), Inches(5.5),
                          how_it_works, size=12)

        # Right: SAP Integration
        self._add_text(slide, Inches(7.0), Inches(2.6), Inches(5.5),
                       Inches(0.35), "S/4 HANA Integration", size=14,
                       bold=True, color=NAVY)
        self._add_bullets(slide, Inches(7.0), Inches(3.0), Inches(5.5),
                          sap_integration, size=12)

        # KPIs bar at bottom
        self._add_text(slide, Inches(0.75), Inches(5.4), Inches(11),
                       Inches(0.35), "Target KPIs", size=14, bold=True,
                       color=NAVY)
        left = Inches(0.75)
        for metric, value in kpis:
            self._box(slide, left, Inches(5.85), Inches(2.8), Inches(0.9),
                      LIGHT_GRAY, "", border_color=color)
            self._add_text(slide, left + Inches(0.15), Inches(5.9),
                           Inches(2.5), Inches(0.4), value, size=20,
                           bold=True, color=color)
            self._add_text(slide, left + Inches(0.15), Inches(6.3),
                           Inches(2.5), Inches(0.35), metric, size=10,
                           color=MED_GRAY)
            left += Inches(3.0)
        self._footer(slide)

    def _slide_demand_forecasting(self, prs):
        self._slide_use_case(
            prs,
            title="Use Case 1 — Demand Forecasting",
            subtitle="Predict dealership demand for vehicles and parts",
            description=(
                "Machine learning models analyze historical sales data, seasonal patterns, "
                "economic indicators, and dealer-specific trends to generate accurate demand "
                "forecasts at SKU level. Forecasts feed directly into S/4 HANA MRP and "
                "distribution planning."
            ),
            how_it_works=[
                "Ingest 3-5 years of dealer order and POS data from SD",
                "Enrich with external signals: economic data, weather, competitor activity",
                "Train ensemble models (XGBoost + LSTM) for short and long-term forecasts",
                "Generate SKU-level forecasts at dealer, region, and national level",
                "Auto-update demand plans in S/4 HANA Demand Management (MD61/MD62)",
                "Continuous model retraining with actual vs. forecast variance feedback",
            ],
            sap_integration=[
                "SD: Sales order history, delivery data, dealer allocation",
                "MM: Material master data, BOM structures, lead times",
                "SAP IBP: Demand planning integration for consensus forecasting",
                "SAP Analytics Cloud: Forecast dashboards and variance reports",
                "SAP BTP: ML model hosting and inference API",
                "Fiori: Demand planner cockpit for exception management",
            ],
            kpis=[
                ("Forecast Accuracy (MAPE)", "< 15%"),
                ("Bias Reduction", "50-70%"),
                ("Stockout Reduction", "30-40%"),
                ("Planning Cycle Time", "60% Faster"),
            ],
            color=ACCENT_BLUE,
        )

    def _slide_inventory_optimization(self, prs):
        self._slide_use_case(
            prs,
            title="Use Case 2 — Inventory Optimization",
            subtitle="Maintain optimal stock across warehouses and dealers",
            description=(
                "AI-driven inventory optimization dynamically adjusts safety stock, reorder "
                "points, and replenishment quantities across the entire network — from national "
                "distribution centres to 280+ individual dealerships — balancing service levels "
                "against carrying costs."
            ),
            how_it_works=[
                "Classify inventory using AI-powered ABC/XYZ segmentation",
                "Calculate dynamic safety stock based on demand variability and lead time",
                "Optimize reorder points per SKU per location using stochastic models",
                "Multi-echelon optimization: national DC → regional DC → dealer",
                "Slow-mover identification and redistribution recommendations",
                "Automatic parameter updates pushed to S/4 HANA Material Master",
            ],
            sap_integration=[
                "MM: Material master, MRP parameters, stock overview (MMBE)",
                "EWM: Warehouse stock, bin locations, throughput data",
                "SD: Dealer stock visibility and replenishment orders",
                "SAP IBP: Inventory optimization integration",
                "MRP: Auto-adjusted safety stock and reorder point via MRP profiles",
                "Fiori: Inventory health dashboard with exception alerts",
            ],
            kpis=[
                ("Excess Inventory", "15-25% \u2193"),
                ("Service Level (OTIF)", "> 97%"),
                ("Carrying Cost Reduction", "12-18%"),
                ("Obsolete Stock", "40% \u2193"),
            ],
            color=GREEN,
        )

    def _slide_supply_planning(self, prs):
        self._slide_use_case(
            prs,
            title="Use Case 3 — Supply Planning",
            subtitle="Adjust procurement and logistics based on predicted demand",
            description=(
                "AI-enhanced supply planning connects demand forecasts to procurement execution, "
                "automatically generating purchase orders, adjusting supplier schedules, and "
                "managing supply constraints. The system proactively identifies supply risks "
                "and recommends alternative sourcing strategies."
            ),
            how_it_works=[
                "Translate AI demand forecasts into net requirements via MRP",
                "Auto-generate purchase requisitions for predicted shortfalls",
                "Supplier performance scoring using delivery/quality history",
                "Lead time prediction using ML models on supplier behaviour",
                "Supply risk monitoring: supplier financial health, geopolitical risk",
                "Scenario planning: what-if analysis for supply disruptions",
            ],
            sap_integration=[
                "MM Procurement: Auto-PO creation, source determination",
                "MRP: AI-adjusted planning parameters and scheduling agreements",
                "SAP Ariba: Supplier collaboration and risk intelligence",
                "SD: Demand signals feeding into supply requirements",
                "S/4 HANA PP: Production planning for locally assembled components",
                "SAP BTP: Supply risk scoring API and ML model hosting",
            ],
            kpis=[
                ("Procurement Cycle Time", "30-40% \u2193"),
                ("Supplier On-Time Delivery", "> 95%"),
                ("Emergency Orders", "50-60% \u2193"),
                ("Cost Avoidance", "8-12% Savings"),
            ],
            color=ORANGE,
        )

    def _slide_logistics_optimization(self, prs):
        self._slide_use_case(
            prs,
            title="Use Case 4 — Logistics Optimization",
            subtitle="Move vehicles and parts efficiently across the network",
            description=(
                "AI optimizes the physical movement of vehicles and parts across Toyota's "
                "Australian distribution network. From vehicle carrier route planning to "
                "parts consolidation and last-mile delivery, the system minimizes transport "
                "costs while maintaining delivery commitments to 280+ dealerships."
            ),
            how_it_works=[
                "Vehicle carrier route optimization using constraint-based algorithms",
                "Parts consolidation: combine dealer orders to maximize truck utilization",
                "Dynamic routing: adjust routes based on real-time traffic and constraints",
                "Load optimization: maximize container/truck fill rates",
                "Delivery window optimization aligned with dealer receiving capacity",
                "Carbon footprint tracking and green logistics recommendations",
            ],
            sap_integration=[
                "SD: Delivery creation, shipping point determination",
                "EWM: Outbound processing, wave management, loading",
                "SAP TM: Transportation management and carrier selection",
                "SAP BN4L: Business Network for Logistics visibility",
                "Yard Management: Vehicle staging and carrier scheduling",
                "Fiori: Transport cockpit with real-time tracking",
            ],
            kpis=[
                ("Transport Cost", "10-15% \u2193"),
                ("Truck Utilization", "> 85%"),
                ("Delivery Lead Time", "20-30% \u2193"),
                ("Carbon Emissions", "12-18% \u2193"),
            ],
            color=TEAL,
        )

    def _slide_benefits(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Benefits & Business Impact")

        categories = [
            ("Financial Benefits", TOYOTA_RED, [
                "15-25% reduction in inventory carrying costs ($15-25M annual savings potential)",
                "10-15% reduction in logistics and transport costs",
                "8-12% procurement cost avoidance through better planning",
                "30-40% reduction in emergency/expedited orders premium",
            ]),
            ("Operational Benefits", ACCENT_BLUE, [
                "20-30% improvement in forecast accuracy driving better decisions",
                "97%+ On-Time-In-Full (OTIF) delivery to dealerships",
                "60% faster demand planning cycles (weeks to days)",
                "50% reduction in manual planning effort through automation",
            ]),
            ("Strategic Benefits", GREEN, [
                "Data-driven decision culture across the supply chain",
                "Competitive advantage through predictive operations",
                "Enhanced dealer satisfaction with improved part availability",
                "Foundation for autonomous supply chain operations",
            ]),
        ]

        top = Inches(1.4)
        for heading, clr, items in categories:
            self._box(slide, Inches(0.75), top, Inches(3.2), Inches(0.45),
                      clr, heading, text_size=13, bold=True)
            bt = top + Inches(0.05)
            for item in items:
                self._add_text(slide, Inches(4.2), bt, Inches(8.5),
                               Inches(0.3), f"\u2022  {item}", size=11,
                               color=DARK_GRAY)
                bt += Inches(0.3)
            top += Inches(1.4)

        # ROI summary
        self._add_text(slide, Inches(0.75), Inches(5.8), Inches(11.5),
                       Inches(0.35), "Estimated ROI: 3-5x return within 24 months of full deployment",
                       size=14, bold=True, color=TOYOTA_RED)
        self._footer(slide)

    def _slide_challenges(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Challenges & Mitigation Strategies")

        challenges = [
            ("Data Quality & Integration",
             "Inconsistent data across dealer systems, legacy data gaps, "
             "varying data standards across 280+ dealerships",
             "Implement data governance framework, MDM (Master Data Management), "
             "phased data cleansing program, SAP Data Intelligence for quality monitoring"),
            ("Change Management",
             "Resistance from planning teams accustomed to manual processes, "
             "dealer adoption of new digital tools and processes",
             "Executive sponsorship, phased rollout starting with pilot dealers, "
             "comprehensive training program, early wins to build momentum"),
            ("Model Accuracy & Trust",
             "ML models need sufficient historical data to be reliable, "
             "black-box concerns from business users",
             "Start with hybrid human+AI approach, explainable AI dashboards, "
             "gradual autonomy increase as trust builds, continuous validation"),
            ("Technical Complexity",
             "Real-time integration across multiple S/4 HANA modules, "
             "ML model deployment and monitoring at scale",
             "SAP BTP as integration platform, microservices architecture, "
             "MLOps framework for model lifecycle, SAP AI Core for deployment"),
            ("Cost & Timeline",
             "Significant investment required for AI infrastructure, data prep, "
             "and organizational change management",
             "Phased approach with quick wins first, start with highest-ROI use case "
             "(demand forecasting), reinvest savings into subsequent phases"),
        ]

        top = Inches(1.35)
        for title, challenge, mitigation in challenges:
            self._box(slide, Inches(0.5), top, Inches(2.5), Inches(0.45),
                      DARK_RED, title, text_size=10, bold=True)
            self._add_text(slide, Inches(3.2), top + Inches(0.02),
                           Inches(4.5), Inches(0.42), challenge, size=10,
                           color=DARK_GRAY)
            self._add_text(slide, Inches(7.9), top + Inches(0.02),
                           Inches(5), Inches(0.42),
                           f"\u2713 {mitigation}", size=10, color=GREEN)
            top += Inches(0.58)

        # Column headers
        self._add_text(slide, Inches(3.2), Inches(4.3), Inches(4), Inches(0.3),
                       "", size=1)

        # Risk matrix note
        self._add_text(slide, Inches(0.5), Inches(4.5), Inches(12), Inches(0.6),
                       "Risk Management Approach: Each challenge is assigned a risk owner, "
                       "monitored via monthly steering committee reviews, and tracked through "
                       "a RAID log integrated with the project management office.",
                       size=12, color=DARK_GRAY)
        self._footer(slide)

    def _slide_architecture(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Technical Architecture — AI on SAP BTP")

        # Layer 1: Presentation
        self._add_text(slide, Inches(0.5), Inches(1.3), Inches(2), Inches(0.3),
                       "PRESENTATION", size=10, bold=True, color=TOYOTA_RED)
        apps = ["Fiori Demand\nPlanner", "Fiori Inventory\nCockpit",
                "Fiori Supply\nMonitor", "SAP Analytics\nCloud"]
        left = Inches(2.5)
        for app in apps:
            self._box(slide, left, Inches(1.25), Inches(2.3), Inches(0.6),
                      LIGHT_GRAY, app, text_size=10, text_color=DARK_GRAY,
                      border_color=ACCENT_BLUE)
            left += Inches(2.6)

        # Layer 2: AI Services
        self._add_text(slide, Inches(0.5), Inches(2.15), Inches(2), Inches(0.3),
                       "AI SERVICES", size=10, bold=True, color=TOYOTA_RED)
        services = ["SAP AI Core\n(Model Training)", "SAP AI Launchpad\n(Model Mgmt)",
                     "Custom ML\n(Python/TensorFlow)", "SAP Data\nIntelligence"]
        left = Inches(2.5)
        for svc in services:
            self._box(slide, left, Inches(2.1), Inches(2.3), Inches(0.6),
                      ACCENT_BLUE, svc, text_size=10, bold=True)
            left += Inches(2.6)

        # Layer 3: Integration
        self._add_text(slide, Inches(0.5), Inches(3.0), Inches(2), Inches(0.3),
                       "INTEGRATION", size=10, bold=True, color=TOYOTA_RED)
        integrations = ["SAP CPI\n(Event Mesh)", "SAP BTP\n(APIs & Events)",
                        "OData Services\n(Real-time)", "Batch Jobs\n(Nightly Sync)"]
        left = Inches(2.5)
        for intg in integrations:
            self._box(slide, left, Inches(2.95), Inches(2.3), Inches(0.6),
                      SAP_GOLD, intg, text_size=10, text_color=DARK_GRAY, bold=True)
            left += Inches(2.6)

        # Layer 4: S/4 HANA Core
        self._add_text(slide, Inches(0.5), Inches(3.85), Inches(2), Inches(0.3),
                       "S/4 HANA CORE", size=10, bold=True, color=TOYOTA_RED)
        modules = ["MM\nProcurement", "MM\nInventory", "EWM\nWarehouse",
                    "SD\nDistribution"]
        colors = [ACCENT_BLUE, GREEN, ORANGE, TEAL]
        left = Inches(2.5)
        for mod, clr in zip(modules, colors):
            self._box(slide, left, Inches(3.8), Inches(2.3), Inches(0.6),
                      clr, mod, text_size=10, bold=True)
            left += Inches(2.6)

        # Layer 5: Data
        self._add_text(slide, Inches(0.5), Inches(4.7), Inches(2), Inches(0.3),
                       "DATA LAYER", size=10, bold=True, color=TOYOTA_RED)
        data = ["SAP HANA DB\n(Transactional)", "SAP Data Warehouse\nCloud",
                "External Data\n(Market, Weather)", "Dealer Systems\n(POS Data)"]
        left = Inches(2.5)
        for d in data:
            self._box(slide, left, Inches(4.65), Inches(2.3), Inches(0.6),
                      NAVY, d, text_size=10, bold=True)
            left += Inches(2.6)

        self._footer(slide)

    def _slide_roadmap(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Implementation Roadmap — Phased Approach")

        phases = [
            ("Phase 1\nFoundation\n(Months 1-4)", ACCENT_BLUE,
             ["Data assessment & cleansing",
              "SAP BTP setup & integration",
              "Demand forecasting MVP",
              "Pilot with 20 dealers"]),
            ("Phase 2\nExpansion\n(Months 5-8)", GREEN,
             ["Inventory optimization rollout",
              "Supply planning automation",
              "Expand to 100 dealers",
              "Model refinement"]),
            ("Phase 3\nOptimization\n(Months 9-12)", ORANGE,
             ["Logistics optimization go-live",
              "Full dealer network rollout",
              "Advanced analytics & reporting",
              "Autonomous decision loops"]),
            ("Phase 4\nScale\n(Months 13-18)", TEAL,
             ["Self-learning optimization",
              "Predictive maintenance integration",
              "Dealer self-service analytics",
              "Continuous improvement"]),
        ]

        left = Inches(0.5)
        for title, clr, items in phases:
            self._box(slide, left, Inches(1.4), Inches(2.8), Inches(1.0),
                      clr, title, text_size=12, bold=True)
            bt = Inches(2.55)
            for item in items:
                self._add_text(slide, left + Inches(0.1), bt,
                               Inches(2.6), Inches(0.28),
                               f"\u2022 {item}", size=10, color=DARK_GRAY)
                bt += Inches(0.3)
            left += Inches(3.1)

        # Arrows between phases
        for i in range(3):
            self._arrow_right(slide, Inches(3.4 + i * 3.1), Inches(1.75))

        # Bottom: key milestones
        self._add_text(slide, Inches(0.5), Inches(4.2), Inches(12), Inches(0.35),
                       "Key Milestones & Gates", size=14, bold=True, color=NAVY)
        milestones = [
            ("Month 2", "Data readiness sign-off"),
            ("Month 4", "Demand forecasting MVP go-live with pilot dealers"),
            ("Month 8", "Inventory + Supply planning live for 100 dealers"),
            ("Month 12", "Full network live with all 4 AI use cases"),
            ("Month 18", "Autonomous supply chain operations achieved"),
        ]
        top = Inches(4.65)
        for date, desc in milestones:
            self._add_text(slide, Inches(0.5), top, Inches(1.5), Inches(0.28),
                           date, size=11, bold=True, color=TOYOTA_RED)
            self._add_text(slide, Inches(2.0), top, Inches(10), Inches(0.28),
                           desc, size=11, color=DARK_GRAY)
            top += Inches(0.3)
        self._footer(slide)

    def _slide_next_steps(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._slide_title(slide, "Next Steps & Recommendations")

        self._add_text(slide, Inches(0.75), Inches(1.4), Inches(11), Inches(0.35),
                       "Immediate Actions (Next 4 Weeks)", size=16, bold=True,
                       color=NAVY)
        immediate = [
            "Conduct data readiness assessment across S/4 HANA modules and dealer systems",
            "Define success criteria and KPIs with Toyota supply chain leadership",
            "Identify pilot dealership group (20 dealers) for Phase 1",
            "Set up SAP BTP environment and confirm AI Core licensing",
            "Establish project governance: steering committee, PMO, RAID log",
        ]
        self._add_bullets(slide, Inches(0.75), Inches(1.85), Inches(11),
                          immediate, size=13)

        self._add_text(slide, Inches(0.75), Inches(3.7), Inches(11), Inches(0.35),
                       "Recommended Engagement Model", size=16, bold=True,
                       color=NAVY)
        engagement = [
            "Phase 1 Discovery Workshop: 2-day workshop to deep-dive into current processes and pain points",
            "Proof of Concept: 8-week demand forecasting PoC with real Toyota data",
            "Business Case Refinement: Update ROI model with PoC results",
            "Full Program Launch: Phased delivery aligned with Toyota planning cycles",
        ]
        self._add_bullets(slide, Inches(0.75), Inches(4.15), Inches(11),
                          engagement, size=13)

        # Contact box
        self._box(slide, Inches(0.75), Inches(5.65), Inches(11.5), Inches(0.9),
                  NAVY, "", border_color=TOYOTA_RED)
        self._add_text(slide, Inches(1.0), Inches(5.75), Inches(11), Inches(0.35),
                       "Ready to begin? Let's schedule a Discovery Workshop to validate "
                       "these AI use cases against Toyota Australia's specific data landscape.",
                       size=14, bold=True, color=WHITE)
        self._add_text(slide, Inches(1.0), Inches(6.15), Inches(11), Inches(0.3),
                       "Proposed Start: Q2 2026  |  Duration: 18 months  |  "
                       "Investment: TBD based on scope confirmation",
                       size=12, color=SAP_GOLD)
        self._footer(slide)

    def _slide_thank_you(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        bg = slide.background.fill
        bg.solid()
        bg.fore_color.rgb = NAVY

        top_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, self.SLIDE_W, Inches(0.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = TOYOTA_RED
        top_bar.line.fill.background()

        self._add_text(slide, Inches(1), Inches(2.8), Inches(11), Inches(1),
                       "Thank You", size=48, bold=True, color=WHITE)
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(1), Inches(3.9), Inches(2), Pt(3))
        line.fill.solid()
        line.fill.fore_color.rgb = TOYOTA_RED
        line.line.fill.background()
        self._add_text(slide, Inches(1), Inches(4.2), Inches(11), Inches(0.6),
                       "Toyota Motors Australia  |  AI-Powered S/4 HANA Transformation",
                       size=18, color=SAP_GOLD)
        self._add_text(slide, Inches(1), Inches(5.2), Inches(11), Inches(0.4),
                       "Confidential — For Discussion Purposes Only",
                       size=12, color=MED_GRAY)
        self._footer(slide, dark=True)

    # ── Main Generator ────────────────────────────────────────

    async def generate(self) -> dict:
        """Generate the complete Toyota AI use case presentation."""
        prs = self._prs()

        # Cover
        self._slide_cover(prs)
        self._slide_agenda(prs)

        # Section 1: Context
        self._section_divider(prs, 1, "Executive Summary",
                              "Business Context & Strategic Objectives")
        self._slide_exec_summary(prs)

        # Section 2: Current State
        self._section_divider(prs, 2, "Current State",
                              "S/4 HANA Modules & Operational Footprint")
        self._slide_current_state(prs)

        # Section 3: Process Flow
        self._section_divider(prs, 3, "AI Process Flow",
                              "End-to-End Integration with S/4 HANA")
        self._slide_process_flow_overview(prs)
        self._slide_detailed_flow(prs)

        # Section 4: Architecture
        self._section_divider(prs, 4, "Technical Architecture",
                              "AI Platform on SAP BTP")
        self._slide_architecture(prs)

        # Section 5: Use Case Deep Dives
        self._section_divider(prs, 5, "AI Use Case Deep Dives",
                              "Demand Forecasting \u2022 Inventory \u2022 Supply Planning \u2022 Logistics")
        self._slide_demand_forecasting(prs)
        self._slide_inventory_optimization(prs)
        self._slide_supply_planning(prs)
        self._slide_logistics_optimization(prs)

        # Section 6: Benefits
        self._section_divider(prs, 6, "Benefits & ROI",
                              "Quantified Business Outcomes")
        self._slide_benefits(prs)

        # Section 7: Challenges
        self._section_divider(prs, 7, "Challenges & Mitigations",
                              "Implementation Risks & Strategies")
        self._slide_challenges(prs)

        # Section 8: Roadmap
        self._section_divider(prs, 8, "Roadmap & Next Steps",
                              "Phased Implementation Approach")
        self._slide_roadmap(prs)
        self._slide_next_steps(prs)

        # Thank You
        self._slide_thank_you(prs)

        return self._save(prs)

    def _save(self, prs) -> dict:
        filename = f"toyota_au_ai_use_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        filepath = os.path.join(OUTPUT_DIR, filename)
        prs.save(filepath)
        return {
            "filename": filename,
            "filepath": filepath,
            "download_url": f"/api/presentations/download/{filename}",
            "slides_count": len(prs.slides),
            "type": "toyota_ai_use_cases",
        }


toyota_ai_generator = ToyotaAIPPTGenerator()
