from fastapi import FastAPI
from backend.routes import donor, chat
from fastapi.middleware.cors import CORSMiddleware

from backend.database.database import engine
from backend.db_models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
         "https://ai-blood-assistant.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Home route
@app.get("/")
def home():
    return {"message": "AI Blood Assistant API running 🚀"}

# ✅ Include routes
app.include_router(donor.router)
app.include_router(chat.router)