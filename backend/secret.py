
import os
import uuid
import base64
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .models import SecretCreate, UserCreate, SecretGet
from . import models
from .bucket import Bucket
from .logger import get_logger
from .encryption import decrypt_string

logger = get_logger()
bucket = Bucket()

def create_secret(secret: SecretCreate, current_user: UserCreate, db: Session):
    """ Create secret """
    #TODO: check for duplicates

    # Generate unique uuid
    secret_uuid = str(uuid.uuid4())

    # Generate the nonce
    nonce = os.urandom(12)
    
    # Grab the master key
    raw_key = os.getenv("ENCRYPTION_KEY")
    if raw_key is None:
        raise ValueError("ENCRYPTION KEY not found")
    key = base64.b64decode(raw_key)

    # Encrypt the secret
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, secret.content.encode(), None)
    encrypted_content = base64.b64encode(nonce + ciphertext).decode()

    # Encode the nonce to store in the database
    nonce = base64.b64encode(nonce)

    # Create database entry
    new_secret = models.Secret(
        name=secret.name,
        type=secret.type,
        note=secret.note,
        nonce=nonce,
        s3_key=secret_uuid
    )

    try:
        # Create secret in database
        db.add(new_secret)
        
        # Create secret in bucket
        bucket.create_object(secret_uuid, encrypted_content)

        db.commit()
        return {"message": f"Succesfully created secret {secret.name}"}

    except Exception as e:
        db.rollback()
        logger.error(f"Could not create secret {secret.name} with UUID {secret_uuid}: {e}")
        return {"message": f"Something went wrong trying to create secret {secret.name}."}

def list_secrets(user: UserCreate, db: Session): 
    try:
        db_secrets = db.query(models.Secret).all()
    
        return {"result": db_secrets}
    except Exception as e:
        logger.error(f"Could not list secrets: {e}")
        return {"message": "Something went wrong trying to list secrets"}

def remove_secret(secret: SecretGet, user: UserCreate, db: Session):
    try:
        db_secret = db.query(models.Secret).filter_by(name=secret.name).first()

        if not db_secret:
            logger.warning(f"No secret named {secret.name} found.")
            return {"message": f"No secret named {secret.name} found."}

        s3_key = db_secret.s3_key

        # Now delete the secret
        db.delete(db_secret)
        db.commit()

        bucket.remove_object(s3_key)

        logger.info(f"Removed secret {secret.name}")
        return {"message": f"Succesfully removed secret {secret.name}"}

    except Exception as e:
        db.rollback()
        logger.error(f"Could not remove secret {e}")
        return {f"message": f"Something went wrong trying to remove secret {secret.name}"}

def get_secret(secret: SecretGet, user: UserCreate, db: Session):

    try:
        db_secret = db.query(models.Secret).filter_by(name=secret.name).first()
        if not db_secret:
            logger.warning(f"No secret named {secret.name} found.")
            return {"message": f"No secret named {secret.name} found."}

        encrypted_content = bucket.get_object(db_secret.s3_key)
        nonce = db_secret.nonce
        
        content = decrypt_string(encrypted_content, nonce)
        
        return(content)

    except Exception as e:
        logger.error(f"Could not get secret {secret.name}: {e}")
        return {"message": f"Something went wrong trying to get secret {secret.name}"}


    

