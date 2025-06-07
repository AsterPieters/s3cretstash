
import uuid
from sqlalchemy.orm import Session

from .models import SecretCreate
from . import models
from .bucket import Bucket

bucket = Bucket()

def create_secret(secret: SecretCreate, db: Session, content):
    """ Create secret """
    #TODO: check for duplicates


    new_secret = models.Secret(
        name=secret.name,
        type=secret.type,
        note=secret.note,
        s3_key=uuid.uuid4()

    )
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)
    
    bucket.create_object(secret.name, content)
