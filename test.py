from modules.bucket import Bucket

bucket = Bucket()
#objects = bucket.list_objects()

#from modules.encryption import encrypt_secret, decrypt_secret



#secret_json = encrypt_secret("test", "asterdafjsfj")
#print(secret_json)

#secret = decrypt_secret("test", secret_json)
#print(secret)

from modules.authentication import register_user, authenticate_user

#register("aster")

#content = bucket.get_object("master_secret")



print(authenticate_user("asters"))
