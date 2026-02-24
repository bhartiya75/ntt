"""Enrichment Service — Enriches stakeholder data from external APIs."""

from typing import Optional
import httpx

from app.config import settings


class EnrichmentService:
    """Enriches stakeholder and company data using Apollo.io and other APIs."""

    async def enrich_from_apollo(self, email: Optional[str] = None, linkedin_url: Optional[str] = None) -> Optional[dict]:
        """Enrich a contact using Apollo.io API.

        Returns structured data about the person and their company.
        Requires APOLLO_API_KEY to be set.
        """
        if not settings.apollo_api_key:
            return None

        if not email and not linkedin_url:
            return None

        try:
            async with httpx.AsyncClient() as client:
                params = {"api_key": settings.apollo_api_key}
                if email:
                    params["email"] = email
                if linkedin_url:
                    params["linkedin_url"] = linkedin_url

                response = await client.post(
                    "https://api.apollo.io/v1/people/match",
                    json=params,
                    timeout=30.0,
                )
                if response.status_code == 200:
                    data = response.json()
                    person = data.get("person", {})
                    if not person:
                        return None

                    org = person.get("organization", {})

                    return {
                        "person": {
                            "first_name": person.get("first_name"),
                            "last_name": person.get("last_name"),
                            "title": person.get("title"),
                            "headline": person.get("headline"),
                            "email": person.get("email"),
                            "phone": person.get("phone_numbers", [{}])[0].get("sanitized_number") if person.get("phone_numbers") else None,
                            "linkedin_url": person.get("linkedin_url"),
                            "city": person.get("city"),
                            "state": person.get("state"),
                            "country": person.get("country"),
                            "seniority": person.get("seniority"),
                            "departments": person.get("departments", []),
                        },
                        "company": {
                            "name": org.get("name"),
                            "domain": org.get("primary_domain"),
                            "industry": org.get("industry"),
                            "sub_industry": org.get("sub_industry"),
                            "employee_count": org.get("estimated_num_employees"),
                            "revenue": org.get("annual_revenue_printed"),
                            "headquarters": f"{org.get('city', '')}, {org.get('country', '')}".strip(", "),
                            "technologies": org.get("current_technologies", []),
                        },
                    }
                return None
        except Exception:
            return None

    def map_apollo_to_stakeholder(self, apollo_data: dict) -> dict:
        """Map Apollo enrichment data to stakeholder fields."""
        person = apollo_data.get("person", {})
        company = apollo_data.get("company", {})

        seniority_map = {
            "c_suite": "c_suite",
            "owner": "c_suite",
            "founder": "c_suite",
            "vp": "vp",
            "director": "director",
            "manager": "manager",
            "senior": "senior",
            "entry": "individual_contributor",
        }

        return {
            "first_name": person.get("first_name"),
            "last_name": person.get("last_name"),
            "email": person.get("email"),
            "phone": person.get("phone"),
            "job_title": person.get("title"),
            "linkedin_url": person.get("linkedin_url"),
            "linkedin_headline": person.get("headline"),
            "linkedin_location": f"{person.get('city', '')}, {person.get('country', '')}".strip(", "),
            "seniority_level": seniority_map.get(person.get("seniority"), person.get("seniority")),
            "department": person.get("departments", [None])[0] if person.get("departments") else None,
            "company_name": company.get("name"),
        }

    def map_apollo_to_company(self, apollo_data: dict) -> dict:
        """Map Apollo enrichment data to company fields."""
        company = apollo_data.get("company", {})

        return {
            "name": company.get("name"),
            "domain": company.get("domain"),
            "industry": company.get("industry"),
            "sub_industry": company.get("sub_industry"),
            "employee_count": str(company.get("employee_count", "")) if company.get("employee_count") else None,
            "revenue_range": company.get("revenue"),
            "headquarters_location": company.get("headquarters"),
        }


enrichment_service = EnrichmentService()
