from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, database
from .bucket import Bucket
from .models import SecretCreate, UserCreate
from .user import get_current_user, register_user, login_user
from .logger import get_logger
from .secret import create_secret

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
logger = get_logger()
bucket = Bucket()

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

@app.get("/bucket/status")
def read_bucket_status(current_user: models.User = Depends(get_current_user)):
    return bucket.bucket_exists_()

@app.post("/secrets/create")
def create_secret_(
        current_user: models.User = Depends(get_current_user),
        secret: SecretCreate,
        content: str
        ):
    return create_secret(secret, content)
