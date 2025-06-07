import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
from urllib3 import PoolManager
from io import BytesIO

from .logger import get_logger

logger = get_logger()


class Bucket:
    def __init__(self):
        
        # Load the credentials from the environment variables
        load_dotenv("bucket_credentials.env")

        http_client = PoolManager(timeout=3.0) 

        self.bucket_name = os.getenv("BUCKET")
        self.client = Minio(
            endpoint=os.getenv("ENDPOINT_URL").replace("https://", "").replace("http://", ""),
            access_key=os.getenv("ACCESS_KEY"),
            secret_key=os.getenv("SECRET_KEY"),
            secure=os.getenv("ENDPOINT_URL").startswith("https"),
            http_client=http_client
        )

        self.bucket_exists_()

    def bucket_exists_(self):
        try:
            exists = self.client.bucket_exists(self.bucket_name)
            if exists:
                logger.info("Bucket exists")
                return True
            else:
                logger.error("Bucket does not exits")
                return False

        except S3Error as e:
            logger.error(f"Bucket does not exist: {e}")
            return False

    def create_object(self, object_name, content):
        
        data = BytesIO(content.encode("utf-8"))

        self.client.put_object(
            self.bucket_name,
            object_name,
            data,
            length=len(content.encode("utf-8")),
            content_type="text/plain"
        )

    def remove_object(self, object_name):

        self.client.remove_object(
            self.bucket_name,
            object_name
        )

