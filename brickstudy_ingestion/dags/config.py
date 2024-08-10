import os
from airflow.models import Variable

# NAVER API
NAVER_API_CLIENT_ID = Variable.get("NAVER_API_CLIENT_ID", "")
NAVER_API_CLIENT_SECERT = Variable.get("NAVER_API_CLIENT_SECERT", "")

# NEWS API
if "NEWSAPI_KEY" not in os.environ:
    os.environ["NEWSAPI_KEY"] = Variable.get("NEWSAPI_KEY", "")

# AWS
AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = Variable.get('BUCKET_NAME', "brickstudy")
S3_BRONZE_BASE_PATH = Variable.get('S3_BRONZE_BASE_PATH', "bronze/")