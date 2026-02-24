"""Stakeholder Profiling Engine — Builds 360° profiles using AI analysis."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.services.ai_engine import ai_engine


class ProfilingService:
    """Analyzes stakeholders and generates comprehensive intelligence profiles."""

    SYSTEM_PROMPT = """You are an expert SAP sales intelligence analyst working for a leading
SAP consulting and implementation firm. You specialize in understanding enterprise
technology buyers, their pain points, and mapping them to relevant SAP solutions.

Your analysis should be actionable for a senior sales executive who needs to have
a highly personalized, value-driven conversation with this stakeholder.

SAP Portfolio you can recommend:
- SAP S/4HANA (Cloud, Private, On-Premise) — ERP transformation
- SAP Business AI — Embedded AI across business processes
- SAP BTP (Business Technology Platform) — Integration, extension, data & analytics
- SAP SuccessFactors — HCM / HR transformation
- SAP Ariba — Procurement & supply chain
- SAP Concur — Travel & expense
- SAP Signavio — Business process intelligence
- SAP Analytics Cloud — Planning & analytics
- SAP Integration Suite — System integration
- SAP Build — Low-code/no-code development
- SAP Datasphere — Data management & warehousing
- RISE with SAP / GROW with SAP — Bundled transformation offerings"""

    async def generate_full_profile(
        self,
        stakeholder: Stakeholder,
        company: Optional[Company],
        provider: str = "claude",
    ) -> dict:
        """Generate a complete AI profile for a stakeholder."""
        context = self._build_context(stakeholder, company)

        prompt = f"""Analyze this stakeholder and provide a comprehensive sales intelligence profile.

{context}

Provide your analysis as JSON with these keys:
{{
    "profile_summary": "2-3 paragraph executive summary of who this person is, what they care about, and why they matter for SAP sales",
    "need_analysis": "What this stakeholder likely needs based on their role, company, and industry. Be specific about business challenges they face.",
    "gap_analysis": "What's missing in their current technology landscape that SAP can address. Identify specific gaps.",
    "pain_points": ["list of 3-5 specific pain points they likely experience"],
    "recommended_sap_solutions": ["list of 2-4 SAP solutions most relevant to them, ordered by relevance"],
    "conversation_starters": ["list of 3-4 personalized conversation openers that would resonate"],
    "best_outreach_channel": "linkedin_message or linkedin_inmail or email — with brief reasoning",
    "engagement_score": 0-100,
    "fit_score": 0-100,
    "key_talking_points": ["3-4 key points to hit in a conversation"],
    "potential_objections": ["2-3 likely objections and how to handle them"],
    "recommended_approach": "Brief strategy for how to approach this person (direct pitch, thought leadership, warm intro, etc.)"
}}"""

        return await ai_engine.generate_json(prompt, self.SYSTEM_PROMPT, provider, max_tokens=3000)

    async def analyze_needs(
        self, stakeholder: Stakeholder, company: Optional[Company], provider: str = "claude"
    ) -> str:
        """Deep dive on what this stakeholder needs."""
        context = self._build_context(stakeholder, company)

        prompt = f"""Based on this stakeholder's profile, provide a detailed need analysis.
Focus on what business challenges they face, what technology gaps exist, and
where SAP solutions could create measurable value.

{context}

Be specific and actionable. Write 3-4 paragraphs."""

        return await ai_engine.generate(prompt, self.SYSTEM_PROMPT, provider)

    async def analyze_gaps(
        self, stakeholder: Stakeholder, company: Optional[Company], provider: str = "claude"
    ) -> str:
        """Identify gaps in the stakeholder's current SAP/tech landscape."""
        context = self._build_context(stakeholder, company)

        prompt = f"""Analyze the technology and process gaps for this stakeholder and their company.
What are they missing? Where could SAP Business AI and other SAP solutions fill gaps?

{context}

Focus on:
1. Technology gaps (missing systems, outdated tools, manual processes)
2. Process gaps (inefficiencies, lack of automation, poor visibility)
3. Strategic gaps (not leveraging AI, missing analytics, poor integration)

Write 3-4 paragraphs with specific, actionable insights."""

        return await ai_engine.generate(prompt, self.SYSTEM_PROMPT, provider)

    async def generate_conversation_starters(
        self, stakeholder: Stakeholder, company: Optional[Company], provider: str = "claude"
    ) -> list[str]:
        """Generate personalized conversation starters."""
        context = self._build_context(stakeholder, company)

        prompt = f"""Generate 5 personalized conversation starters for reaching out to this stakeholder.
Each should feel natural, reference something specific about them or their company,
and subtly connect to SAP value without being salesy.

{context}

Return as JSON: {{"starters": ["starter1", "starter2", ...]}}"""

        result = await ai_engine.generate_json(prompt, self.SYSTEM_PROMPT, provider)
        return result.get("starters", [])

    def _build_context(self, stakeholder: Stakeholder, company: Optional[Company]) -> str:
        """Build context string from stakeholder and company data."""
        parts = ["STAKEHOLDER INFORMATION:"]
        parts.append(f"Name: {stakeholder.full_name}")
        if stakeholder.job_title:
            parts.append(f"Title: {stakeholder.job_title}")
        if stakeholder.seniority_level:
            parts.append(f"Seniority: {stakeholder.seniority_level}")
        if stakeholder.department:
            parts.append(f"Department: {stakeholder.department}")
        if stakeholder.linkedin_headline:
            parts.append(f"LinkedIn Headline: {stakeholder.linkedin_headline}")
        if stakeholder.linkedin_summary:
            parts.append(f"LinkedIn Summary: {stakeholder.linkedin_summary}")
        if stakeholder.linkedin_location:
            parts.append(f"Location: {stakeholder.linkedin_location}")
        if stakeholder.current_sap_experience:
            parts.append(f"SAP Experience: {stakeholder.current_sap_experience}")
        if stakeholder.interests:
            parts.append(f"Interests: {', '.join(stakeholder.interests)}")
        if stakeholder.content_topics:
            parts.append(f"Content Topics: {', '.join(stakeholder.content_topics)}")
        if stakeholder.career_history:
            parts.append(f"Career History: {stakeholder.career_history}")
        if stakeholder.pain_points:
            parts.append(f"Known Pain Points: {', '.join(stakeholder.pain_points)}")

        if company:
            parts.append("\nCOMPANY INFORMATION:")
            parts.append(f"Company: {company.name}")
            if company.industry:
                parts.append(f"Industry: {company.industry}")
            if company.sub_industry:
                parts.append(f"Sub-Industry: {company.sub_industry}")
            if company.employee_count:
                parts.append(f"Employees: {company.employee_count}")
            if company.revenue_range:
                parts.append(f"Revenue: {company.revenue_range}")
            if company.headquarters_location:
                parts.append(f"HQ: {company.headquarters_location}")
            if company.current_erp:
                parts.append(f"Current ERP: {company.current_erp}")
            if company.current_sap_products:
                parts.append(f"Current SAP Products: {', '.join(company.current_sap_products)}")
            if company.sap_maturity_level:
                parts.append(f"SAP Maturity: {company.sap_maturity_level}")
            if company.known_pain_points:
                parts.append(f"Company Pain Points: {', '.join(company.known_pain_points)}")
        elif stakeholder.company_name:
            parts.append(f"\nCompany: {stakeholder.company_name}")

        return "\n".join(parts)


profiling_service = ProfilingService()
