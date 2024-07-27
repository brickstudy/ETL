import os
from typing import Any

import boto3

from src.common.aws_s3_mime import EXTENSION_TO_MIME

#TODO s3 client object 생성자에서 받아서 초기화? is refactor needed?
class S3Uploader:
    def __init__(self) -> None:
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.s3_client = None

    def write_s3(
            self,
            bucket_name: str, 
            file_key: str,
            data_type: str,
            data: Any
        )-> None:

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id, 
            aws_secret_access_key=self.aws_secret_access_key
        )

        self.s3_client.put_object(
            Bucket=bucket_name, 
            Key=file_key, 
            Body=data,
            ContentType=self.get_mime_type(data_type)
        )

    @staticmethod
    def get_mime_type(extension: str):
        if extension not in EXTENSION_TO_MIME: 
            raise ValueError("Unsupported file extension.")
        return EXTENSION_TO_MIME.get(extension) 