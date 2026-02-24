"""Segmentation Service — Groups stakeholders into targetable segments."""

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.stakeholder import Stakeholder
from app.models.company import Company


class SegmentationService:
    """Segments stakeholders based on various criteria for 1-to-many campaigns."""

    def segment_stakeholders(
        self, db: Session, filters: dict
    ) -> list[Stakeholder]:
        """Filter stakeholders based on segment criteria.

        Supported filters:
        - seniority_levels: list of seniority levels
        - departments: list of departments
        - industries: list of industries (via company)
        - sap_maturity_levels: list of SAP maturity levels (via company)
        - priority_tiers: list of tier numbers (via company)
        - min_engagement_score: minimum engagement score
        - min_fit_score: minimum fit score
        - tags: list of tags (stakeholder must have at least one)
        - company_ids: list of company IDs
        - decision_maker_types: list of decision maker types
        - buying_stages: list of buying stages
        """
        query = db.query(Stakeholder)
        conditions = []

        if filters.get("seniority_levels"):
            conditions.append(
                Stakeholder.seniority_level.in_(filters["seniority_levels"])
            )

        if filters.get("departments"):
            conditions.append(Stakeholder.department.in_(filters["departments"]))

        if filters.get("company_ids"):
            conditions.append(Stakeholder.company_id.in_(filters["company_ids"]))

        if filters.get("decision_maker_types"):
            conditions.append(
                Stakeholder.decision_maker_type.in_(filters["decision_maker_types"])
            )

        if filters.get("buying_stages"):
            conditions.append(
                Stakeholder.buying_stage.in_(filters["buying_stages"])
            )

        if filters.get("min_engagement_score"):
            conditions.append(
                Stakeholder.engagement_score >= filters["min_engagement_score"]
            )

        if filters.get("min_fit_score"):
            conditions.append(
                Stakeholder.fit_score >= filters["min_fit_score"]
            )

        # Apply company-level filters via join
        needs_company_join = any(
            filters.get(k)
            for k in ["industries", "sap_maturity_levels", "priority_tiers"]
        )

        if needs_company_join:
            query = query.join(Company, Stakeholder.company_id == Company.id)
            if filters.get("industries"):
                conditions.append(Company.industry.in_(filters["industries"]))
            if filters.get("sap_maturity_levels"):
                conditions.append(
                    Company.sap_maturity_level.in_(filters["sap_maturity_levels"])
                )
            if filters.get("priority_tiers"):
                conditions.append(
                    Company.priority_tier.in_(filters["priority_tiers"])
                )

        if conditions:
            query = query.filter(and_(*conditions))

        return query.all()

    def get_segment_summary(self, stakeholders: list[Stakeholder]) -> dict:
        """Generate a summary of a stakeholder segment."""
        if not stakeholders:
            return {"count": 0}

        seniority_dist = {}
        department_dist = {}
        company_dist = {}

        for s in stakeholders:
            if s.seniority_level:
                seniority_dist[s.seniority_level] = (
                    seniority_dist.get(s.seniority_level, 0) + 1
                )
            if s.department:
                department_dist[s.department] = (
                    department_dist.get(s.department, 0) + 1
                )
            if s.company_name:
                company_dist[s.company_name] = (
                    company_dist.get(s.company_name, 0) + 1
                )

        return {
            "count": len(stakeholders),
            "seniority_distribution": seniority_dist,
            "department_distribution": department_dist,
            "companies": company_dist,
            "avg_engagement_score": (
                sum(s.engagement_score or 0 for s in stakeholders) / len(stakeholders)
            ),
            "avg_fit_score": (
                sum(s.fit_score or 0 for s in stakeholders) / len(stakeholders)
            ),
        }


segmentation_service = SegmentationService()
