from fastapi import APIRouter
from backend.database.database import SessionLocal
from backend.db_models import DonorDB

router = APIRouter()

@router.get("/chat")
def chat(query: str):
    db = SessionLocal()

    donors = db.query(DonorDB).all()

    results = []
    query_clean = query.strip().lower()

    for d in donors:
        if query_clean in d.blood.lower() or query_clean in d.location.lower():
            results.append(f"{d.name}, {d.blood}, {d.location}")

    db.close()

    if not results:
        return {"results": ["No donors found"]}

    return {"results": results}