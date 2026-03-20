from sqlalchemy import Column, Integer, String
from backend.database.database import Base

class DonorDB(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    blood = Column(String)
    location = Column(String)