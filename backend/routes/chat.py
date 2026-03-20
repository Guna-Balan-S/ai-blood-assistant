from fastapi import APIRouter
from backend.database.database import SessionLocal
from backend.db_models import DonorDB

router = APIRouter()

@router.get("/chat")
def chat(query: str):
    db = SessionLocal()
    query = query.lower().strip()

    words = query.split()

    # ------------------ ADD ------------------
    if query.startswith("add"):
        try:
            name = words[1]
            blood = words[2]
            location = words[3]

            donor = DonorDB(name=name, blood=blood, location=location)
            db.add(donor)
            db.commit()
            db.close()

            return {"results": [f"✅ Donor {name} added successfully"]}

        except:
            return {"results": ["❌ Format: add name blood location"]}

    # ------------------ UPDATE ------------------
    if query.startswith("update"):
        try:
            name = words[1]
            blood = words[2]
            location = words[3]

            donor = db.query(DonorDB).filter(DonorDB.name.ilike(name)).first()

            if donor:
                donor.blood = blood
                donor.location = location
                db.commit()
                db.close()
                return {"results": [f"✏️ {name} updated successfully"]}
            else:
                return {"results": ["❌ Donor not found"]}

        except:
            return {"results": ["❌ Format: update name blood location"]}

    # ------------------ DELETE ------------------
    if query.startswith("delete"):
        try:
            name = words[1]

            donor = db.query(DonorDB).filter(DonorDB.name.ilike(name)).first()

            if donor:
                db.delete(donor)
                db.commit()
                db.close()
                return {"results": [f"🗑️ {name} deleted successfully"]}
            else:
                return {"results": ["❌ Donor not found"]}

        except:
            return {"results": ["❌ Format: delete name"]}

    # ------------------ SEARCH ------------------
    results = []

    for d in db.query(DonorDB).all():
        if query in d.blood.lower() or query in d.location.lower() or query in d.name.lower():
            results.append(f"{d.name}, {d.blood}, {d.location}")

    db.close()

    if results:
        return {"results": results}

    return {"results": ["No donors found"]}