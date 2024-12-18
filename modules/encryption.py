# encryption.py

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import base64
import json
import os

def encrypt_secret(master_secret, plain_text_secret):
    """
    Encrypt a plain text secret using the master secret.

    Args:
        master_secret (str): The master secret.
        plain_text_secret (str): The to be encrypted secret in plain text.
    
    Returns:
        str: A JSON string containing the salt, iv and encrypted secret.
    """
    try:
        # Generate a random salt
        salt = os.urandom(16)

        # Key derivation function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )

        # Derive the key from the master secret
        encryption_key = kdf.derive(master_secret.encode("utf-8"))

        # Generate a random initialization vector
        iv = os.urandom(12)
        
        # Encrypt the secret
        aesgcm = AESGCM(encryption_key)
        encrypted_secret = aesgcm.encrypt(iv, plain_text_secret.encode("utf-8"), None)

        # Construct and return a dictionary
        data = {
            "salt": base64.b64encode(salt).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
            "secret": base64.b64encode(encrypted_secret).decode("utf-8")
        }

        return data

    except Exception as e:
        raise ValueError(f"Error occured while trying to encrypt secret: {e}")



def decrypt_secret(master_secret, secret_data_json):
    """
    Decrypt a secret using the master secret.

    Args:
        master_secret (str): The master secret.
        secret_data_json (str): A JSON string with the salt, IV, and encrypted secret.
    
    Returns:
        plain_text_secret (str): The decrypted plain text secret.
    """
    try:
        # Parse the JSON string into a dictionary
        secret_data = json.loads(secret_data_json)

        # Decode the Base64-encoded values
        salt = base64.b64decode(secret_data['salt'])
        iv = base64.b64decode(secret_data['iv'])
        secret = base64.b64decode(secret_data['secret'])

        # Key derivation function
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )

        # Derive the key from the master secret
        encryption_key = kdf.derive(master_secret.encode('utf-8'))

        # Decrypt the secret
        aesgcm = AESGCM(encryption_key)
        decrypted_secret = aesgcm.decrypt(iv, secret, None)
        plain_text_secret = decrypted_secret.decode()

        return plain_text_secret

    except Exception as e:
        print(f"Error occurred while trying to decrypt secret: {e}")



def hash_secret(secret, salt=None):
    """
    Hashes the secret.

    Args:
        secret (str): A secret.
        salt (str): The salt to use.

    Returns:
        json_hashed_secret (JSON): A dictionary with the salt and hashed_secret.    
    """
    if not salt:
        # Generate a random salt
        salt = os.urandom(16)

    # Key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )

    # Hash the secret
    secret_hash = kdf.derive(secret.encode('utf-8'))

    # Put the values in a dictionary
    return json.dumps({
        "salt": base64.b64encode(salt).decode('utf-8'),
        "secret_hash": base64.b64encode(secret_hash).decode('utf-8')
    })

