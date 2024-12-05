#authentication.py
import json
import base64

from .logger import s3cretstashlogger
from .encryption import hash_secret
from .miniobucket import MinioBucket

logger = s3cretstashlogger()

def register(master_secret, bucket):
    """Register the user

    Args:
        master_secret (str): The master secret.
    
    Returns:
        str: A JSON string containing the salt and hash.
    """
    try:
        # Hash the data
        hashed_data = hash_secret(master_secret)
         
        # Write the data to s3
        bucket.create_object("master_secret", hashed_data)

        logger.info("Created object master_secret.")

    except Exception as e:
        raise ValueError(f"Error occured while trying to register: {e}")



def authenticate(master_secret):
    """Authenticate the user

    Args:
        master_secret (str): The master secret.
    
    Returns:
        bool: True if the master secret matches.
    """
    try:

        # bucket
        bucket = MinioBucket()

        # Get the data from the bucket and load as json
        data = bucket.get_object("master_secret")
        data = json.loads(data)
        
        # Extract the values
        salt = base64.b64decode(data["salt"])
        hashed_master_secret = base64.b64decode(data["secret_hash"])

        # Hash the inputted master_secret
        input_data = hash_secret(master_secret, salt=salt)
        input_data = json.loads(input_data)
        input_hashed_master_secret = base64.b64decode(input_data["secret_hash"])

        if hashed_master_secret == input_hashed_master_secret:
            return True
        else:
            return False
                                  
    except Exception as e:
        print(f"Error occured while trying to authenticate user: {e}")
        return False
