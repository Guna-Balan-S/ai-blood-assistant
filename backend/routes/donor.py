from fastapi import APIRouter
from backend.database.database import SessionLocal
from backend.db_models import DonorDB

router = APIRouter(prefix="/api")

@router.post("/add-donor")
def add_donor(data: dict):
    db = SessionLocal()

    donor = DonorDB(
        name=data["name"],
        blood=data["blood"],
        location=data["location"]
    )

    db.add(donor)
    db.commit()
    db.refresh(donor)

    db.close()

    return {"message": "Donor added"}

@router.get("/donors")
def get_donors():
    db = SessionLocal()
    donors = db.query(DonorDB).all()
    db.close()

    return [
        {
            "name": d.name,
            "blood": d.blood,
            "location": d.location
        }
        for d in donors
    ]