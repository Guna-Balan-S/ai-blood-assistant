from sqlalchemy import Column, Integer, String
from backend.database.database import Base

# 🔴 Donor Table
class DonorDB(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    blood = Column(String)
    location = Column(String)


# 🔐 User Table (NEW)
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)