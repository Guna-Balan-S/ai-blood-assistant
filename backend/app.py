from fastapi import FastAPI
from backend.routes import auth, donor
from fastapi.middleware.cors import CORSMiddleware
import sys
import os  

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(donor.router)