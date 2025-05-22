from fastapi import HTTPException
import os
from minio.error import S3Error, InvalidResponseError
from minio import Minio
import uuid

from .models import Objectstorage, ObjectstorageAccess
from .settings import fernet

def add_objectstorage(objectstorage, current_user, db):
    """ Add objectstorage to platform """
    # Check if objectstorage with that name already exists
    existing = db.query(Objectstorage).filter_by(name=objectstorage.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Objectstorage with that name alreay exists")

    # Check if the objectspace is accessible
    client = create_client(objectstorage)
    objectstorage_exists(client)

    # Encrypt the secret key before storing it in the database
    encrypted_secret_key = fernet.encrypt(objectstorage.secret_key.encode())

    # Create the objectstorage in the database
    new_objectstorage = Objectstorage(
        name=objectstorage.name,
        access_key=objectstorage.access_key,
        secret_key=encrypted_secret_key,
        endpoint_url=objectstorage.endpoint_url,
public=objectstorage.public
        )
    db.add(new_objectstorage)
    db.commit()
    db.refresh(new_objectstorage)

    # Create the objectstorageaccess
    objectstorage_access = ObjectstorageAccess(
        user_id=current_user.id,
        objectstorage_id=new_objectstorage.id
    )
    db.add(objectstorage_access)
    db.commit()

    return {"message": "Objectstorage created"}

def list_objectstorages(current_user, db):
    """ List available objectstorages for the user """
    
    # Grab all objectstorages for the user
    access_entries = db.query(ObjectstorageAccess).filter_by(user_id=current_user.id).all()
    objectstorage_ids = [entry.objectstorage_id for entry in access_entries]

    if not objectstorage_ids:
        return {"message": "No objectstorages found"}

    # Grab the name and endpoint_url
    results = (
        db.query(Objectstorage.name, Objectstorage.endpoint_url)
        .filter(Objectstorage.id.in_(objectstorage_ids))
        .all()
    )

    return [{"name": name, "endpoint_url": endpoint_url} for name, endpoint_url in results]

def create_client(objectstorage):
    """
    Create client to connect to the objectstorage
    """
    
    # Create the client using the variables
    client = Minio(
            endpoint=objectstorage.endpoint_url, 
            access_key=objectstorage.access_key,
            secret_key=objectstorage.secret_key, 
            secure=True)
    
    return client

def objectstorage_exists(client):
    try:
        # List buckets as a simple auth check
        client.list_buckets()
        return {"message": "Objectstorage exists"}

    except S3Error as err:
        raise HTTPException(status_code=500, detail=f"S3 error (possibly invalid credentials): {err}")
    except InvalidResponseError as err:
        raise HTTPException(status_code=500, detail=f"Invalid response: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Other error: {e}")
