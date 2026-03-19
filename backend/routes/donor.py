@router.post("/add-donor")
def add_donor(donor: dict):
    donors.append(donor)
    return {"message": "Donor added"}