#secrets.py

from .encryption import encrypt_secret, decrypt_secret
from .miniobucket import MinioBucket

import base64

def add_secret(secret_name, secret, user):
    """
    Encrypt and add secret to the bucket.
    
    Args:
        secret_name (STR): The name of the secret.
        secret (STR): The secret to be encrypted.
    """

    # Encrypt the secret
    secret_data = encrypt_secret(user.master_secret, secret)

    # base64 the secret_name
    object_name = base64.b64encode(secret_name.encode('utf-8')).decode('utf-8')

    bucket = MinioBucket()
    
    # Create the object
    bucket.create_object(object_name, secret_data)

def delete_secret(secret_name):
    """
    Delete secret from bucket.

    Args:
        secret_name (STR): The name of the secret.
    """

    print(secret_name)

    # base64 the secret name
    object_name = base64.b64encode(secret_name.encode('utf-8')).decode('utf-8')

    bucket = MinioBucket()

    # Delete the object
    bucket.delete_object(object_name)

def list_secrets():
    """
    List all secrets stored.
    
    """
    decoded_secrets = []
    bucket = MinioBucket()

    # Fetch all objects
    secrets = bucket.list_objects()

    # Remove the master secret
    secrets.remove('master_secret')

    # Decode the secret_name
    for secret in secrets:
        decoded_secret = base64.b64decode(secret).decode('utf-8')
        decoded_secrets.append(decoded_secret)

    return decoded_secrets     

def get_secrets(master_secret):
    """
    Get all stored secrets and decrypt them.

    Args:
        master_secret: The master secret.

    Returns:
        data: 
    """
    secrets = []
    bucket = MinioBucket()

    # Get all objects
    objects = bucket.list_objects()
    objects.remove("master_secret")


    for object in objects:

        # Decode the object 
        secret_name = base64.b64decode(object).decode('utf-8')

        # Get the data out of the object
        secret_data = bucket.get_object(object)
        
        # Decrypt the data
        secret_value = decrypt_secret(master_secret, secret_data)

        # Create dict for secret
        secret = {
            "secret_name": secret_name,
            "secret_value": secret_value
                }

        # Add dict to list
        secrets.append(secret)

    return secrets 
    
