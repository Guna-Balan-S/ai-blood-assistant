from fastapi import APIRouter, Depends
from backend.database.database import SessionLocal
from backend.db_models import DonorDB
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/api")

@router.post("/add-donor")
def add_donor(data: dict, user_id: int = Depends(get_current_user)):
    db = SessionLocal()

    donor = DonorDB(
        name=data["name"],
        blood=data["blood"],
        location=data["location"]
    )

    db.add(donor)
    db.commit()
    db.close()

    return {"message": "Donor added"}

@router.get("/donors")
def get_donors(user_id: int = Depends(get_current_user)):
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