from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

def _t1(ti):
    #1st way :: return is the 1st way for XCOM, this value after DAG successful will also be visible on Admin->xcoms
    #return 55
    #2nd Way :: ti=taskInstance
    print(ti.xcom_push(key='my_key', value=65))

def _t2(ti):
    ti.xcom_pull(key='my_key', task_ids='t1')

def _branch(ti):
    value = ti.xcom_pull(key='my_key', task_ids='t1')
    if value == 65:
        return 't2'
    return 't3'

with DAG("xcom_dag", start_date=datetime(2022, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    t1=PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    branch=BranchPythonOperator(
        task_id='branch',
        python_callable=_branch
    )

    t2=PythonOperator(
        task_id='t2',
        python_callable=_t2
    )    

    t3=BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )        

    t4=BashOperator(
        task_id='t4',
        bash_command="echo ''",
        trigger_rule='one_success'
    )   

    t1 >> branch >> [t2, t3] >> t4