from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 Password hash
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# 🔐 Create JWT
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔐 Get current user
def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# 🚀 Register
@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    user = UserDB(
        username=data["username"],
        password=hash_password(data["password"]),
        blood=data["blood"],
        location=data["location"]
    )
    db.add(user)
    db.commit()
    return {"message": "User registered"}

# 🚀 Login
@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = filter(UserDB.username == data["username"]).first()

    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id})

    return {"access_token": token}