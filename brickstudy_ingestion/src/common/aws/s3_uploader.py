import os
import json
from typing import Any

import boto3

from src.common.aws.s3_mime import EXTENSION_TO_MIME


class S3Uploader:
    def __init__(self) -> None:
        self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )

    def write_s3(
            self,
            file_key: str,
            data_type: str,
            data: Any,
            bucket_name: str = "brickstudy",
    ) -> None:

        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=self.ensure_json_string(data),
            ContentType=self.get_mime_type(data_type)
        )

    @staticmethod
    def get_mime_type(extension: str):
        if extension not in EXTENSION_TO_MIME:
            raise ValueError("Unsupported file extension.")
        return EXTENSION_TO_MIME.get(extension)

    @staticmethod
    def ensure_json_string(data):
        if isinstance(data, str):
            try:
                json.loads(data)
                return data
            except json.JSONDecodeError:
                pass
        return json.dumps(data)
