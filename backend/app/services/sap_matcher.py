"""SAP Solution Matcher — Matches stakeholders to the most relevant SAP solutions."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.stakeholder import Stakeholder
from app.models.company import Company
from app.models.sap_solution import SAPSolution
from app.services.ai_engine import ai_engine


class SAPMatcher:
    """Matches stakeholders and companies to relevant SAP solutions."""

    SYSTEM_PROMPT = """You are an SAP solution architect who deeply understands the full
SAP portfolio and can match business needs to the right SAP solutions.
You consider the stakeholder's role, industry, company size, current tech stack,
and pain points to recommend the most relevant solutions."""

    async def match_solutions(
        self,
        stakeholder: Stakeholder,
        company: Optional[Company],
        available_solutions: list[dict],
        provider: str = "claude",
    ) -> list[dict]:
        """Match a stakeholder to the most relevant SAP solutions."""
        from app.services.profiling import profiling_service

        context = profiling_service._build_context(stakeholder, company)

        solutions_text = "\n".join(
            f"- {s['solution_name']} ({s['category']}): {s.get('description', 'N/A')}"
            for s in available_solutions
        )

        prompt = f"""Given this stakeholder profile, rank and recommend the most relevant SAP solutions.

{context}

AVAILABLE SAP SOLUTIONS:
{solutions_text}

Return as JSON:
{{
    "recommendations": [
        {{
            "solution_name": "name",
            "relevance_score": 0-100,
            "reasoning": "why this is relevant to this specific person",
            "talking_point": "one sentence to use when discussing this with them",
            "use_case": "specific use case for their industry/role"
        }}
    ]
}}

Order by relevance_score descending. Include top 3-5 solutions only."""

        result = await ai_engine.generate_json(prompt, self.SYSTEM_PROMPT, provider)
        return result.get("recommendations", [])


sap_matcher = SAPMatcher()
