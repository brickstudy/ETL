import json
import requests
from datetime import datetime

from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator



def send_discord_message():
    connection = BaseHook.get_connection('discord_webhook')
    url = connection.host
    headers = {"Content-Type": "application/json"}
    data = {
        "content": "Airflow에서 보내는 테스트 메시지입니다."
    }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
    response.raise_for_status()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 10),
}

with DAG(
    dag_id='discord_webhook_dag',
    default_args=default_args,
    schedule_interval=None,
) as dag:

    send_message_task = PythonOperator(
        task_id='send_discord_message',
        python_callable=send_discord_message,
    )

    send_message_task
