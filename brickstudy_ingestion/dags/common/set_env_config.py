from airflow import DAG
from airflow.models import Variable, Connection
from airflow.utils.dates import days_ago
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.python import PythonOperator
from airflow.utils.db import provide_session

# =========================================
"""
Description:
수동 설정 필요한 connections
    - MYSQL_CONN_URL
수동 설정 필요한 variables
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
"""

# Set aiflow setting
default_args = {
    'owner': 'brickstudy',
    'start_date': days_ago(1),
}
# =========================================


@provide_session
def set_airflow_env_var(session=None, **context):
    """ airflow 테이블에서 가져온 데이터를 Ariflow Connection으로 설정하는 함수 """
    query_results = context['task_instance'].xcom_pull(task_ids='get_airflow_env_vars')

    if not query_results:
        raise ValueError("No data received from MySQL query")

    for id_, type_, host_ in query_results:
        conn = Connection(
            conn_id=id_,
            conn_type=type_,
            host=host_
        )
        existing_conn = session.query(Connection).filter(Connection.conn_id == conn.conn_id).first()
        if existing_conn:
            session.delete(existing_conn)
            session.commit()
        session.add(conn)
        session.commit()


def set_media_env_var(**context):
    """ media 테이블에서 가져온 데이터를 Airflow variables로 설정하는 함수 """
    query_results = context['task_instance'].xcom_pull(task_ids='get_media_env_vars')

    # set env variables
    for source_, client_id, client_pw in query_results:
        env_name = source_.upper()
        if client_id:
            Variable.set(env_name + "_CLIENT_ID", client_id)
            # print(f"{env_name}_CLIENT_ID set to: {client_id}")
        if client_pw:
            Variable.set(env_name + "_CLIENT_PW", client_pw)
            # print(f"{env_name}_CLIENT_PW set to: {client_pw}")


with DAG(
    dag_id='0_set_airflow_env_variable',
    default_args=default_args,
    schedule_interval='0 0,12 * * *',
    catchup=False,
) as dag:
    # Run airflow table query
    get_airflow_env_vars = MySqlOperator(
        task_id='get_airflow_env_vars',
        mysql_conn_id='MYSQL_CONN_URL',
        sql='SELECT id_, type_, host_ FROM brickas.airflow;',   # TODO: connection 늘어나면 수정
    )

    # Set airflow env variables
    set_airflow_env_var = PythonOperator(
        task_id='set_airflow_env_var',
        python_callable=set_airflow_env_var,
        provide_context=True,
    )

    # Run media table query
    get_media_env_vars = MySqlOperator(
        task_id='get_media_env_vars',
        mysql_conn_id='MYSQL_CONN_URL',
        sql='SELECT source_, client_id, client_pw FROM brickas.media;',
    )

    # Set media env variables
    set_media_env_var = PythonOperator(
        task_id='set_media_env_var',
        python_callable=set_media_env_var,
        provide_context=True,
    )

    get_airflow_env_vars >> set_airflow_env_var
    get_media_env_vars >> set_media_env_var
