from airflow.models import Variable


NAVER_API_CLIENT_ID = Variable.get("NAVER_API_CLIENT_ID", "")
NAVER_API_CLIENT_SECERT = Variable.get("NAVER_API_CLIENT_SECERT", "")

AWS_ACCESS_KEY_ID = Variable.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY", "")
S3_BUCKET_NAME = Variable.get('BUCKET_NAME', "brickstudy")
S3_BRONZE_BASE_PATH = Variable.get('S3_BRONZE_BASE_PATH', "bronze/")