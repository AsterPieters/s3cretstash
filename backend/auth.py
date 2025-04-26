from passlib.context import CryptContext
from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta

from . import models
from .database import get_db

# should be set in .env
SECRET_KEY = "aster"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """ Hashes password for secure storage in the database """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """ Compares password to hashed password in the database """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """ Compare email and password to authenticate user """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

