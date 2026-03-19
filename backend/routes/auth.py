from fastapi import APIRouter
from backend.database.db import users

router = APIRouter()

@router.post("/register")
def register(user: dict):
    users.append(user)
    return {"message": "User registered"}

@router.post("/login")
def login(user: dict):
    for u in users:
        if u["username"] == user["username"] and u["password"] == user["password"]:
            return {"message": "Login successful"}
    return {"message": "Invalid credentials"}