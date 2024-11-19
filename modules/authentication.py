#authentication.py
import json
import base64

from .encryption import hash_secret
from .bucket import Bucket

def register_user(master_secret):
    """Register the user

    Args:
        master_secret (str): The master secret.
    
    Returns:
        str: A JSON string containing the salt and hash.
    """
    bucket = Bucket()

    try:
        # Hash the data
        hashed_data = hash_secret(master_secret)
         
        # Write the data to s3
        bucket.create_object("master_secret", hashed_data)
        

    except Exception as e:
        raise ValueError(f"Error occured while trying to register: {e}")



def authenticate_user(master_secret):
    """Authenticate the user

    Args:
        master_secret (str): The master secret.
    
    Returns:
        bool: True if the master secret matches.
    """
    bucket = Bucket()
    try:
        # Get the data from S3
        hashed_data = bucket.get_object("master_secret")
        secret_data = json.loads(hashed_data)
        salt = base64.b64decode(secret_data["salt"])
        hashed_master_secret = base64.b64decode(secret_data["secret_hash"])

        # Hash the inputted master_secret
        hashed_data = hash_secret(master_secret, salt=salt)
        secret_data = json.loads(hashed_data)
        inputted_hashed_master_secret = base64.b64decode(secret_data["secret_hash"])



        if hashed_master_secret == inputted_hashed_master_secret:
            return True
        else:
            return False
                                  
    except Exception as e:
        print(f"Error occured while trying to authenticate user: {e}")
        return False
