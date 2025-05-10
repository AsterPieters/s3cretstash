from pydantic_core.core_schema import str_schema
from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, DateTime, Boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    """ Validate user registration data """
    username: str
    email: EmailStr
    password: str

class Objectstorage(Base):
    """ Objectstorage """
    __tablename__ = "objectstorages"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # Access credentials to create buckets
    access_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    endpoint_url = Column(String, nullable=False)

    # Allow all users to access objectstorage
    public = Column(Boolean, nullable=False)

class ObjectstorageCreate(BaseModel):
    name: str
    access_key: str
    secret_key: str
    endpoint_url: str
    public: bool

class ObjectstorageAccess(Base):
    __tablename__ = "objectstorage_access"

    id = Column(Integer, primary_key=True)
    objectstorage_id = Column(Integer, ForeignKey("objectstorages.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class Bucket(Base):
    """ Bucket """
    __tablename__ = "buckets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    objectstorage_id = Column(Integer, ForeignKey("objectstorages.id"))

    # Credentials to access the bucket
    access_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)

    # Encryption key used for file encryption before uploading it to the bucket
    encryption_key = Column(LargeBinary, nullable=False)

class BucketCreate(BaseModel):
    name: str
    objectspace_name: str
    access_key: str
    secret_key: str

class BucketAccess(Base):
    __tablename__ = "bucket_access"

    id = Column(Integer, primary_key=True)
    bucket_id = Column(Integer, ForeignKey("buckets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class File(Base):
    __tablename__ = "files" 
    
    id = Column(Integer, primary_key=True)
    bucket_id = Column(Integer, ForeignKey("buckets.id"))
    name = Column(String)
    s3_key = Column(String) # Formatted name
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    bucket_id = Column(Integer, ForeignKey("buckets.id"))
    name = Column(String)
    note = Column(String)
    s3_key = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
