from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='discord_webhook_dag',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    
    send_discord_message = SimpleHttpOperator(
        task_id='send_discord_message',
        http_conn_id='discord_webhook',
        endpoint='',
        method='POST',
        headers={"Content-Type": "application/json"},
        data='{"content": "Airflow에서 보내는 테스트 메시지입니다."}',
    )

    send_discord_message
