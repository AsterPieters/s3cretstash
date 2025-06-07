
import uuid
from sqlalchemy.orm import Session

from .models import SecretCreate, SecretRemove, UserCreate
from . import models
from .bucket import Bucket
from .logger import get_logger
from .database import get_db

logger = get_logger()
bucket = Bucket()

def create_secret(secret: SecretCreate, current_user: UserCreate, db: Session):
    """ Create secret """
    #TODO: check for duplicates

    # Generate unique uuid
    secret_uuid = str(uuid.uuid4())

    new_secret = models.Secret(
        name=secret.name,
        type=secret.type,
        note=secret.note,
        s3_key=secret_uuid

    )

    try:
        db.add(new_secret)
        db.commit()
        db.refresh(new_secret)
        
        bucket.create_object(secret_uuid, secret.content)
    
        return {"message": f"Succesfully created secret {secret.name}"}

    except Exception as e:
        logger.error(f"Could not create secret {secret.name} with UUID {secret_uuid}: {e}")
        return {"message": f"Something went wrong trying to create secret {secret.name}."}

def list_secrets(user: UserCreate, db: Session): 
    try:
        db_secrets = db.query(models.Secret).all()
    
        return {"result": db_secrets}
    except Exception as e:
        logger.error(f"Could not list secrets: {e}")
        return {"message": "Something went wrong trying to list secrets"}

def remove_secret(secret: SecretRemove, user: UserCreate, db: Session):
    try:
        db_secret = db.query(models.Secret).filter_by(name=secret.name).first()

        if not db_secret:
            logger.warning(f"No secret named '{secret.name}' found for user {user.username}")
            return {"message": f"No secret named '{secret.name}' found."}

        s3_key = db_secret.s3_key

        # Now delete the secret
        db.delete(db_secret)
        db.commit()

        bucket.remove_object(s3_key)

        logger.info(f"Removed secret {secret.name}")
        return {"message": f"Succesfully removed secret {secret.name}"}

    except Exception as e:
        db.rollback()
        logger.error(f"Could not remove secret {secret.name}")
        return {f"message": f"Something went wrong trying to remove secret {e}"}
