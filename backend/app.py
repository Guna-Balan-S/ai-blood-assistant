from fastapi import FastAPI
from backend.routes import donor, chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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