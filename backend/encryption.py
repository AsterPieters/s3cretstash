
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .logger import get_logger
logger = get_logger()

def decrypt_string(encrypted_content_b64, nonce_b64):
   
    try:
        # Load and decode the master key
        raw_key = os.getenv("ENCRYPTION_KEY")
        if raw_key is None:
            raise ValueError("ENCRYPTION_KEY not found")
        key = base64.b64decode(raw_key)

        # Decode the base64-encoded encrypted content
        data = base64.b64decode(encrypted_content_b64)
        nonce, ciphertext = data[:12], data[12:]

        # Decrypt
        aesgcm = AESGCM(key)
        content = aesgcm.decrypt(nonce, ciphertext, None)
        return content
    
    except Exception as e:
        logger.error(f"Could not decrypt string: {e}")



