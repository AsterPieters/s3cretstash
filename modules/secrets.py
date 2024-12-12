#secrets.py

from .encryption import encrypt_secret
from .miniobucket import MinioBucket


import base64

def add_secret(secret_name, secret, user):
    """
    Encrypt and add secret to the bucket.
    
    Args:
        secret_name (STR): The name of the secret.
        secret (STR): The secret to be encrypted.

    Returns:
        idk
    """

    # Encrypt the secret
    secret_data = encrypt_secret(user.master_secret, secret)

    # base64 the secret_name
    object_name = base64.b64encode(secret_name.encode('utf-8')).decode('utf-8')

    bucket = MinioBucket()
    
    # Create the object
    bucket.create_object(object_name, secret_data)


def get_secrets():
    """
    Get all secrets from the bucket.

    Args:
        user: The user object

    Returns:
        idk yet
    """
    decoded_secrets = []


    bucket = MinioBucket()

    # Fetch all objects
    secrets = bucket.list_objects()

    # Remove the master secret
    secrets.remove('master_secret')

    # Decode the secret_name
    for secret in secrets:
        decoded_bytes = base64.b64decode(secret)
        decoded_secret = decoded_bytes.decode('utf-8')
        decoded_secrets.append(decoded_secret)

    return decoded_secrets

    
