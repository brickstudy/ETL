from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount

# from dags.utils.discord_message import on_failure_callback

# =========================================
# Change parameter
DAG_ID = "bronze_viral_twitter"
TARGET_PLATFORM = "twitter"

# Set aiflow setting
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    # 'on_failure_callback': on_failure_callback,
}
# =========================================


OUTPUT_FILENAME = "test.csv"
SEARCH_KEYWORD = "enhypen"
LIMIT = 10
TOKEN = Variable.get("TWITTER_CRAWLER_AUTH_TOKEN_PASSWORD")

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
):
    twitter_crawler_docker_task = DockerOperator(
        task_id='t_docker',
        image='brickstudy/twitter_crawler:latest',
        container_name='twitter_crawler',
        auto_remove=True,
        mount_tmp_dir=False,
        mounts=[
            Mount(source="/opt/airflow/logs/tweets-data", target="/app/tweets-data", type="bind"),
        ],
        command=[
            f"npx --yes tweet-harvest@latest -o {OUTPUT_FILENAME} -s {SEARCH_KEYWORD} -l {LIMIT} --token {TOKEN}"
        ],
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
    )

    twitter_crawler_docker_task
