from fastapi import HTTPException
import os
from fastapi import HTTPException
from minio.error import S3Error

from .settings import fernet
from .models import Bucket, Objectstorage
from .objectstorage import create_client, objectstorage_exists



def list_buckets(current_user, db):
    """ List all bucket created by the user """
    buckets = db.query(Bucket).filter_by(owner_id=current_user.id).all()
    return buckets

def add_bucket(bucket,objectstorage, current_user, db):
    """ Add bucket to objectspace """

    # Check if user already has a bucket with that name
    existing = db.query(Bucket).filter_by(owner_id=current_user.id, name=bucket.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bucket with that name already exists")
    
    # Check if objectstore exists in database
    objectstorage = db.query(Objectstorage).filter_by(name=objectstorage.name).first()
    if not objectstorage:
        raise HTTPException(status_code=500, detail="Objectspace does not exist")

    try:
        # Attempt to create the bucket
        client = create_client(objectstorage)
        client.make_bucket(bucket.name)

    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Generate the encryption key
    encryption_key = os.urandom(32)

    # Encrypt the encryption key using the MASTER KEY
    encrypted_key = fernet.encrypt(encryption_key)

    new_bucket = Bucket(
        name=bucket.name,
        encryption_key=encrypted_key,
        owner_id=current_user.id,
        objectstorage_id=objectstorage.id,
    )

    db.add(new_bucket)
    db.commit()
    db.refresh(new_bucket)

    return {"message": "Bucket created"}

