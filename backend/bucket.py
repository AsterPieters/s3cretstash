from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Security
import os

from .settings import fernet
from .database import get_db
from .models import Bucket, BucketCreate, BucketAccess




def list_buckets(current_user, db):
    """ List all bucket created by the user """
    buckets = db.query(Bucket).filter_by(owner_id=current_user.id).all()
    return buckets

def add_bucket(bucket, current_user, db):
    """ Add bucket to user account """
    # Check if user already has a bucket with that name
    existing = db.query(Bucket).filter_by(owner_id=current_user.id, name=bucket.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bucket with that name already exists")
    
    # Generate the encryption key
    encryption_key = os.urandom(32)

    # Encrypt the encryption key using the MASTER KEY
    encrypted_key = fernet.encrypt(encryption_key)

    new_bucket = Bucket(
        name=bucket.name,
        access_key=bucket.access_key,
        secret_key=bucket.secret_key,
        endpoint_url=bucket.endpoint_url,
        encryption_key=encrypted_key,
        owner_id=current_user.id
    )

    db.add(new_bucket)
    db.commit()
    db.refresh(new_bucket)

    return {"message": "Bucket created"}

