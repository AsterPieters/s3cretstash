from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, database
from .models import UserCreate
from .user import get_current_user, register_user, login_user
from .bucket import add_bucket, list_buckets

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "S3cretstash backend is running"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    return register_user(user, db)

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(database.get_db)):
    return login_user(user, db)

@app.get("/users/me")
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.post("/stashes/add")
def add_stash_api(
    bucket: models.StashCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
    ):
    return add_stash(stash, current_user, db)

@app.post("/buckets/add")
def add_bucket_api(
    bucket: models.BucketCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
    ):
    return add_bucket(bucket, current_user, db)
        
@app.get("/buckets/list")
def list_buckets_api(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(database.get_db)
    ):
    return list_buckets(current_user, db)

@app.post("/passwords/add")
def add_password_api(
    
    bucket: models.BucketCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
    ):
    return add_bucket(bucket, current_user, db)
