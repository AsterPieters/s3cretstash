from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, auth
from .models import UserCreate





def register_user(user: UserCreate, db: Session):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = models.User(
        username=user.username,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered"}





