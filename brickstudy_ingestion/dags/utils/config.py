import os
from airflow.models import Variable


"""
Description:
- 새로운 매체 환경변수 추가 시 아래에 variable 추가해야 합니다!!
(TODO, 변수 아래처럼 직접 입력 없이 airflow 메타데이터에서 바로 가져올 수 있도록 수정 필요)
"""


# SET VARIABLES
def set_env_variables():
    ALL_ENV_VARIABLES = [
        # NAVER API
        "NAVERSEARCH_CLIENT_ID",
        "NAVERSEARCH_CLIENT_PW",
        # NEWS API
        "NEWSAPI_CLIENT_ID",
        # AWS
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY"
    ]
    for ENV_VARIABLE in ALL_ENV_VARIABLES:
        os.environ[ENV_VARIABLE] = Variable.get(ENV_VARIABLE, "")
