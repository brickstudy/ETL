import os
from typing import Any

import boto3

from src.common.aws_s3_mime import EXTENSION_TO_MIME


class S3Uploader:
    def __init__(self) -> None:
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    def write_s3(
            self,
            bucket_name: str, 
            file_key: str,
            data_type: str,
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
            Body=data,
            ContentType=self.get_mime_type(data_type)
        )

    @staticmethod
    def get_mime_type(extension: str):
        if extension not in EXTENSION_TO_MIME: 
            raise ValueError("Unsupported file extension.")
        return EXTENSION_TO_MIME.get(extension) 