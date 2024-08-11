import os
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator


def set_env_vars(**context):
    """ MySQL에서 가져온 데이터를 환경 변수로 설정하는 함수 """
    query_results = context['task_instance'].xcom_pull(task_ids='get_env_vars')

    # set env variables
    for env_name, client_id, client_pw in query_results:
        if client_id:
            os.environ[env_name + "_CLIENT_ID"] = client_id
            # print(f"{env_name}_CLIENT_ID set to: {client_id}")
        if client_pw:
            os.environ[env_name + "_CLIENT_PW"] = client_pw
            # print(f"{env_name}_CLIENT_PW set to: {client_pw}")


default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='set_airflow_env_variable',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Run mysql query
    get_env_vars = MySqlOperator(
        task_id='get_env_vars',
        mysql_conn_id='MYSQL_CONN_URL',
        sql='SELECT env_name, client_id, client_pw FROM brickas.media;',
    )

    # Set env variables
    set_env_var = PythonOperator(
        task_id='set_env_var',
        python_callable=set_env_vars,
        provide_context=True,
    )

    get_env_vars >> set_env_var
