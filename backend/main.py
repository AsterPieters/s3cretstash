from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, database
from .models import UserCreate
from .user import register_user

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "S3cretstash backend is running"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    return register_user(user, db)
