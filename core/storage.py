import json
import boto3
from config import settings

class S3Manager:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name="auto"
        )
        self.bucket = settings.S3_BUCKET_NAME

    def list_raw_files(self):
        res = self.s3.list_objects_v2(Bucket=self.bucket)
        return [obj['Key'] for obj in res.get('Contents', []) 
                if not obj['Key'].startswith('processed_chunks/')]

    def get_file_content(self, key):
        return self.s3.get_object(Bucket=self.bucket, Key=key)['Body'].read()

    def save_chunks_to_s3(self, file_key, chunks):
        path = f"processed_chunks/{file_key}.json"
        json_data = json.dumps(chunks, indent=4, ensure_ascii=False)
        self.s3.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=json_data.encode('utf-8'),
            ContentType="application/json"
        )