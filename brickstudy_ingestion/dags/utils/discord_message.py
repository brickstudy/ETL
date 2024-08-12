import json
import requests

from airflow.hooks.base import BaseHook

"""
# 기본 인자에 추가
default_args = {
    'on_failure_callback': on_failure_callback,
}

"""


def send_discord_message(message):
    connection = BaseHook.get_connection('DISCORD_WEBHOOK')
    url = connection.host
    headers = {"Content-Type": "application/json"}
    data = {
        "content": message
    }

    response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
    if response.status_code != 204:
        raise ValueError(f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}")
    # response.raise_for_status()


def on_success_callback(context):
    """ 성공 시 메시지 전송 함수"""
    send_discord_message(f"DAG {context['dag'].dag_id} succeeded!")


def on_failure_callback(context):
    """ 실패 시 메시지 전송 함수"""
    message = (
        "[Airflow Task 실패 알림]\n"
        f"* DAG: {context['dag'].dag_id}\n"
        f"* Task: {context['task_instance'].task_id}\n"
        f"* Execution Date: {context['execution_date']}\n\n"
        "Airflow를 확인해주세요!!\n"
    )
    send_discord_message(message)
