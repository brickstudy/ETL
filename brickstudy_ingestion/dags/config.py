import os
from airflow.models import Variable

#TODO : 변수 아래처럼 직접 입력 없이 airflow 메타데이터에서 바로 가져올 수 있도록!!
# SET VARIABLES
ALL_ENV_VARIABLES = [
    # AWS
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY"
    # MYSQL
    "MYSQL_CONN_URL"
]

for ENV_VARIABLE in ALL_ENV_VARIABLES:
    os.environ[ENV_VARIABLE] = Variable.get(ENV_VARIABLE, "")
