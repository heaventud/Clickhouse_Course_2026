from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.clickhousedb.hooks.clickhouse import ClickHouseHook


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def transfer_postgres_to_clickhouse(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_dellstore')
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_default')

    select_query = """
       SELECT p.prod_id,                           
              p.category,                           
              c.categoryname,                           
              p.title,                           
              p.actor,                           
              p.price,                           
              COALESCE(p.special, 0) as special,                           
              p.common_prod_id
       FROM products p
       JOIN categories c ON p.category = c.category;
    """

    pg_conn = pg_hook.get_conn()
    with pg_conn.cursor() as cursor:
        cursor.execute(select_query)
        rows = cursor.fetchall()

    if not rows:
        print("No data")
        return

    ch_hook.bulk_insert_rows(
        'products',
        rows,
        ['prod_id', 'category', 'category_name', 'title', 'actor', 'price', 'special', 'common_prod_id'],
    )
    print(f"{len(rows)} rows have been transferred")


with DAG(
        'dellstore_to_clickhouse',
        default_args=default_args,
        description='ETL to ClickHouse',
        schedule='*/1 * * * *',
        is_paused_upon_creation=True,
        catchup=False,
) as dag:
    transfer_task = PythonOperator(
        task_id='transfer_products_data',
        python_callable=transfer_postgres_to_clickhouse,
    )
