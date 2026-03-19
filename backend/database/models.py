# Models
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Donor(BaseModel):
    name: str
    blood: str
    location: str