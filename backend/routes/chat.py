from fastapi import APIRouter
from backend.database.database import SessionLocal
from backend.db_models import DonorDB
import re

router = APIRouter()

# 🔥 Extract blood + location from sentence
def parse_query(query: str):
    query = query.lower()

    blood_patterns = ["o+", "a+", "b+", "ab+", "o-", "a-", "b-", "ab-"]
    found_blood = None

    for b in blood_patterns:
        if b in query:
            found_blood = b
            break

    # remove symbols for easier location match
    clean_query = re.sub(r'[^a-zA-Z ]', '', query)

    words = clean_query.split()

    # assume last word could be location
    location = words[-1] if len(words) > 0 else None

    return found_blood, location


@router.get("/chat")
def chat(query: str):
    db = SessionLocal()
    donors = db.query(DonorDB).all()

    blood, location = parse_query(query)

    results = []

    for d in donors:
        d_blood = d.blood.lower()
        d_location = d.location.lower()

        # 🔥 Smart matching
        if blood and location:
            if blood == d_blood and location in d_location:
                results.append(f"{d.name}, {d.blood}, {d.location}")

        elif blood:
            if blood == d_blood:
                results.append(f"{d.name}, {d.blood}, {d.location}")

        elif location:
            if location in d_location:
                results.append(f"{d.name}, {d.blood}, {d.location}")

    db.close()

    if results:
        return {"results": results}

    return {"results": ["No donors found"]}