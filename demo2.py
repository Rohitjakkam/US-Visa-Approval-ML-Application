import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Ensure AWS credentials are set in environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Example function to list objects in a bucket
def list_s3_objects(bucket_name):
    try:
        s3 = boto3.client('s3', 
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            print(obj['Key'])
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
    except Exception as e:
        print(f"Error: {e}")

list_s3_objects('usvisa-model1')
