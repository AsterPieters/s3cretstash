
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    """ Validate user registration data """
    username: str
    email: EmailStr
    password: str
