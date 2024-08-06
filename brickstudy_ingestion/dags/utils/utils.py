import boto3

from src.naver.naver_search import NaverSearch
from src.common.aws.s3_uploader import S3Uploader
from dags.config import (
    NAVER_API_CLIENT_ID,
    NAVER_API_CLIENT_SECERT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME
)


def request_naver_api(TARGET_PLATFORM, QUERY):
    client = NaverSearch(
        client_id=NAVER_API_CLIENT_ID,
        client_secret=NAVER_API_CLIENT_SECERT,
        target_platform=TARGET_PLATFORM
    )
    return client.request_with_keyword(
        query=QUERY,
        display=100
    )


def upload_to_s3(file_key: str, data):
    s3_client = boto3.client(
        "s3", 
        aws_access_key_id=AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3_uploader = S3Uploader(s3_client)
    s3_uploader.write_s3(
        bucket_name=S3_BUCKET_NAME,
        file_key=file_key,
        data_type='json',
        data=data
    )