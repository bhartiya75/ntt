"""Seed script to load SAP solutions into the database."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.sap_solution import SAPSolution

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Load solutions from JSON
data_path = os.path.join(os.path.dirname(__file__), "app", "data", "sap_solutions.json")
with open(data_path) as f:
    solutions = json.load(f)

count = 0
for sol in solutions:
    existing = db.query(SAPSolution).filter(SAPSolution.solution_name == sol["solution_name"]).first()
    if existing:
        print(f"  Skipping {sol['solution_name']} (already exists)")
        continue

    db_solution = SAPSolution(
        solution_name=sol["solution_name"],
        category=sol["category"],
        description=sol.get("description"),
        target_personas=sol.get("target_personas", []),
        target_industries=sol.get("target_industries", []),
        target_company_size=sol.get("target_company_size", []),
        key_value_props=sol.get("key_value_props", []),
        pain_points_addressed=sol.get("pain_points_addressed", []),
        competitive_differentiators=sol.get("competitive_differentiators", []),
        talk_tracks=sol.get("talk_tracks", []),
        case_studies=sol.get("case_studies", []),
        objection_handlers=sol.get("objection_handlers", []),
    )
    db.add(db_solution)
    count += 1
    print(f"  Added: {sol['solution_name']}")

db.commit()
db.close()

print(f"\nSeeded {count} SAP solutions.")
