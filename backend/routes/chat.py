from fastapi import APIRouter
from backend.database.db import donors

router = APIRouter()

@router.get("/chat")
def chat(query: str):
    results = []
    
    query_clean = query.strip().lower() 

    for d in donors:
        name = str(d.get("name", "Unknown"))

        blood = str(d.get("blood", "")).lower()

        # ✅ FIX HERE
        location_data = d.get("location", "")

        if isinstance(location_data, dict):
            location = str(location_data.get("city", "")).lower()
        else:
            location = str(location_data).lower()

        if query_clean == blood or query_clean in location:
            results.append(f"{name}, {blood.upper()}, {location.capitalize()}")

    if not results:
        return {"results": ["No donors found"]}

    return {"results": results}