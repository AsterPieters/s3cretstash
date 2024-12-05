#initiate_bucket.py

from modules.miniobucket import MinioBucket
from modules.encryption import hash_secret



bucket = MinioBucket()

# Create the master_secret
master_secret = "aster"
hashed_data = hash_secret(master_secret)

bucket.create_object("master_secret", hashed_data)
