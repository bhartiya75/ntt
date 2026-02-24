"""CSV Import/Export API — Import LinkedIn data from CSV files."""

import io
import csv
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stakeholder import Stakeholder
from app.models.company import Company

router = APIRouter(prefix="/import", tags=["import"])

# Common LinkedIn Sales Navigator CSV column mappings
LINKEDIN_CSV_MAPPINGS = {
    # LinkedIn export columns → our fields
    "first name": "first_name",
    "first_name": "first_name",
    "last name": "last_name",
    "last_name": "last_name",
    "full name": "full_name",
    "name": "full_name",
    "email": "email",
    "email address": "email",
    "phone": "phone",
    "phone number": "phone",
    "job title": "job_title",
    "title": "job_title",
    "position": "job_title",
    "company": "company_name",
    "company name": "company_name",
    "organization": "company_name",
    "linkedin url": "linkedin_url",
    "linkedin profile": "linkedin_url",
    "profile url": "linkedin_url",
    "person linkedin url": "linkedin_url",
    "headline": "linkedin_headline",
    "linkedin headline": "linkedin_headline",
    "summary": "linkedin_summary",
    "about": "linkedin_summary",
    "location": "linkedin_location",
    "city": "linkedin_location",
    "connections": "linkedin_connections",
    "# connections": "linkedin_connections",
    "industry": "_industry",
    "company industry": "_industry",
    "company size": "_employee_count",
    "employees": "_employee_count",
    "company domain": "_domain",
    "website": "_domain",
    "seniority": "seniority_level",
    "seniority level": "seniority_level",
    "department": "department",
    "departments": "department",
    "tags": "_tags",
}


@router.post("/linkedin-csv")
async def import_linkedin_csv(
    file: UploadFile = File(...),
    source: str = "csv_import",
    db: Session = Depends(get_db),
):
    """Import stakeholders from a LinkedIn CSV export.

    Supports:
    - LinkedIn Connections export
    - LinkedIn Sales Navigator export
    - Apollo.io export
    - Custom CSV with standard column names
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    text = content.decode("utf-8-sig")  # handle BOM
    reader = csv.DictReader(io.StringIO(text))

    imported = 0
    skipped = 0
    errors = []
    companies_created = {}

    for row_num, row in enumerate(reader, start=2):
        try:
            # Map CSV columns to our fields
            mapped = {}
            company_data = {}

            for csv_col, value in row.items():
                if not value or not value.strip():
                    continue
                normalized_col = csv_col.strip().lower()
                our_field = LINKEDIN_CSV_MAPPINGS.get(normalized_col)

                if our_field:
                    if our_field.startswith("_"):
                        # Company-level field
                        company_data[our_field[1:]] = value.strip()
                    else:
                        mapped[our_field] = value.strip()

            # Build full_name if not present
            if "full_name" not in mapped:
                first = mapped.get("first_name", "")
                last = mapped.get("last_name", "")
                if first or last:
                    mapped["full_name"] = f"{first} {last}".strip()

            if not mapped.get("full_name"):
                skipped += 1
                continue

            # Handle connections as integer
            if "linkedin_connections" in mapped:
                try:
                    mapped["linkedin_connections"] = int(
                        mapped["linkedin_connections"].replace(",", "").replace("+", "")
                    )
                except ValueError:
                    del mapped["linkedin_connections"]

            # Find or create company
            company_id = None
            company_name = mapped.get("company_name")
            if company_name:
                if company_name in companies_created:
                    company_id = companies_created[company_name]
                else:
                    existing = (
                        db.query(Company)
                        .filter(Company.name == company_name)
                        .first()
                    )
                    if existing:
                        company_id = existing.id
                    else:
                        new_company = Company(
                            name=company_name,
                            industry=company_data.get("industry"),
                            employee_count=company_data.get("employee_count"),
                            domain=company_data.get("domain"),
                        )
                        db.add(new_company)
                        db.flush()
                        company_id = new_company.id
                    companies_created[company_name] = company_id

            # Check for duplicate (by LinkedIn URL or name+company)
            duplicate = None
            if mapped.get("linkedin_url"):
                duplicate = (
                    db.query(Stakeholder)
                    .filter(Stakeholder.linkedin_url == mapped["linkedin_url"])
                    .first()
                )
            if not duplicate and mapped.get("email"):
                duplicate = (
                    db.query(Stakeholder)
                    .filter(Stakeholder.email == mapped["email"])
                    .first()
                )

            if duplicate:
                skipped += 1
                continue

            # Create stakeholder
            stakeholder = Stakeholder(
                full_name=mapped.get("full_name"),
                first_name=mapped.get("first_name"),
                last_name=mapped.get("last_name"),
                email=mapped.get("email"),
                phone=mapped.get("phone"),
                linkedin_url=mapped.get("linkedin_url"),
                linkedin_headline=mapped.get("linkedin_headline"),
                linkedin_summary=mapped.get("linkedin_summary"),
                linkedin_connections=mapped.get("linkedin_connections"),
                linkedin_location=mapped.get("linkedin_location"),
                job_title=mapped.get("job_title"),
                seniority_level=mapped.get("seniority_level"),
                department=mapped.get("department"),
                company_id=company_id,
                company_name=company_name,
                source=source,
            )
            db.add(stakeholder)
            imported += 1

        except Exception as e:
            errors.append({"row": row_num, "error": str(e)})

    db.commit()

    return {
        "imported": imported,
        "skipped": skipped,
        "companies_created": len(companies_created),
        "errors": errors[:20],  # limit error reporting
        "total_rows": imported + skipped + len(errors),
    }


@router.post("/manual")
async def import_manual_contacts(
    contacts: list[dict],
    db: Session = Depends(get_db),
):
    """Import contacts from a structured JSON list."""
    imported = 0
    for contact in contacts:
        if not contact.get("full_name"):
            continue

        # Find or create company
        company_id = None
        if contact.get("company_name"):
            existing = (
                db.query(Company)
                .filter(Company.name == contact["company_name"])
                .first()
            )
            if existing:
                company_id = existing.id
            else:
                new_company = Company(name=contact["company_name"])
                db.add(new_company)
                db.flush()
                company_id = new_company.id

        stakeholder = Stakeholder(
            full_name=contact["full_name"],
            first_name=contact.get("first_name"),
            last_name=contact.get("last_name"),
            email=contact.get("email"),
            linkedin_url=contact.get("linkedin_url"),
            linkedin_headline=contact.get("linkedin_headline"),
            job_title=contact.get("job_title"),
            seniority_level=contact.get("seniority_level"),
            department=contact.get("department"),
            company_id=company_id,
            company_name=contact.get("company_name"),
            source="manual",
        )
        db.add(stakeholder)
        imported += 1

    db.commit()
    return {"imported": imported}
