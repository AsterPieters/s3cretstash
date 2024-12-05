#miniobucket.py

from .logger import s3cretstashlogger

import os
import io
from minio import Minio
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO

logger = s3cretstashlogger()

class MinioBucket:
    def __init__(self):
        self.create_client()
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    def create_client(self):
        """
        Create the client using variables in the .env file
        """

        # Load the variables
        load_dotenv() 
        
        # Create the client using the variables
        self.client = Minio(
                endpoint=os.getenv("S3_ENDPOINT_URL"), 
                access_key=os.getenv("S3_ACCESS_KEY"),
                secret_key=os.getenv("S3_SECRET_KEY"), 
                secure=True)

    def create_directory(self, directory_name):
        """"
        Create a directory in the bucket
        """
        try:
            empty_object = BytesIO(b"")
            self.client.put_object(
                self.bucket_name,
                directory_name,
                data=empty_object,
                length=0,
                content_type="application/x-directory"
                )

        except Exception as e:
            logger.error(f"Error occured while trying to create directory {directory_name}: {e}")

    def create_object(self, object_name, data):
        """
        Create an object in the bucket.

        Args:
            object_name (STR): The name of the object to be created.
            data: The data to be stored as JSON.

        """
        try:
            
            # Encode and create file object from the bytes
            data_bytes = data.encode('utf-8')
            data_file = BytesIO(data_bytes)

            # Create the object
            self.client.put_object(
                    self.bucket_name, 
                    object_name, 
                    data_file, 
                    length=len(data),
                    content_type='application/json'
                )
            logger.info(f"Created object {object_name}")

        except Exception as e:
            logger.error(f"Error occured while creating object {object_name}: {e}")

    def get_object(self, object_name):
        """
        Get the object and read its content.

        Args:
            object_name (STR): Name of the object to be fetched.

        Returns:
            data: The parsed JSON data.
        """

        try:
            # Fetch the data from the bucket
            content = self.client.get_object(self.bucket_name, object_name)

            # Read the content and decode it
            data = content.read()
            data.decode('utf-8')

            logger.info(f"Fetched object {object_name}.")
            return data 

        except Exception as e:
            logger.error(f"Error occurred while fetching object {object_name}: {e}")

    def list_objects(self):
        """
        List the objects in the bucket.
        """
        try:
            objects = self.client.list_objects(self.bucket_name)
            for obj in objects:
                print(obj.object_name)
        except Exception as e:
            print(f"Error occurred while listing objects in bucket {self.bucket_name}: {e}")
