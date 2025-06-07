from pydantic_core.core_schema import str_schema
from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, DateTime, Boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Integer, index=True)

class UserCreate(BaseModel):
    """ Validate user registration data """
    username: str
    email: EmailStr
    password: str

class Secret(Base):
    __tablename__ = "secret"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Integer, index=True)
    note = Column(String)
    s3_key = Column(String) # Formatted name to store in bucket
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class SecretCreate(BaseModel):
    name: str
    note: str
