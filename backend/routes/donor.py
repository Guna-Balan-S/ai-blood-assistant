from fastapi import APIRouter
from backend.database.db import donors

router = APIRouter()

@router.post("/add-donor")
def add_donor(donor: dict):
    donors.append(donor)
    return {"message": "Donor added successfully"}

@router.get("/donors")
def get_donors():
    return {"donors": donors}