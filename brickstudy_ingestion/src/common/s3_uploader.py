import os, json
from datetime import datetime
from typing import Any

import boto3


class S3Uploader:
    def __init__(self) -> None:
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    def write_s3(
            self,
            bucket_name: str, 
            file_key: str,
            data: Any
        )-> None:

        s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id, 
            aws_secret_access_key=self.ws_secret_access_key
        )

        s3.put_object(
            Bucket=bucket_name, 
            Key=file_key, 
            Body=json.dumps(data),
            ContentType='application/json'
        )
