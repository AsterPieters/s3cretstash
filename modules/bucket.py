#Bucket.py

import os
import json
import boto3
from dotenv import load_dotenv


class Bucket:

    def __init__(self):
        self.create_client()


    def create_client(self):
        """Create the client using the variables in the .env file"""
        
        # Load the variables
        load_dotenv()

        # Create the client
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY")
        )

        # Load the bucket_name
        self.bucket_name = os.getenv("S3_BUCKET_NAME")


    def list_objects(self):
        """List the objects in the bucket"""
        try:
            
            # Get the objects
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(f"{obj['Key']}")
            else:
                print("Bucket is empty.")
        except Exception as e:
            print(f"Error occured while trying to list objects in bucket {self.bucket_name} {e}")



    def create_object(self, object_name, content):
        """Create an object"""
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=object_name, Body=content)
            print(f"Created object {object_name}") 

        except Exception as e:
            print(f"Error occured while trying to create object {e}")
    


    def get_object(self, object_name):
        """Get the content of an object"""
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
            content = response['Body'].read().decode('utf-8')
            return content

        except Exception as e:
            print(f"Error occurred while trying to get object {e}")
