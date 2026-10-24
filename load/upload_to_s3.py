import os
import boto3
from botocore.exceptions import ClientError

def upload_to_s3():
    bucket = os.getenv('AWS_S3_BUCKET_NAME')
    file_name = 'data/transformed/IBM_cleaned.csv'
    object_name = 'processed/IBM_cleaned.csv'
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to s3://{bucket}/{object_name}")
    except ClientError as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    upload_to_s3()