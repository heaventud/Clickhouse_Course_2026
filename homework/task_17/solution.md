## AirFlow integration with Clickhouse

1. Migration in Clickhouse

```sql
CREATE DATABASE IF NOT EXISTS dellstore;

CREATE TABLE IF NOT EXISTS dellstore.products (
    prod_id Int32,
    category Int32,
    title String,
    actor String,
    price Decimal(12, 2),
    special Int16,
    common_prod_id Int32,
    category_name String,

    updated_at DateTime DEFAULT now()
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY prod_id;
```

2. Airflow DAG task

[dag.py](./airflow/dellstore_dag.py)

![job in Airflow UI](./screen.png)

3. Shell commands

show task metadata
```bash
$ airflow dags details dellstore_to_clickhouse
```

job test run 
```bash
$ airflow tasks test dellstore_to_clickhouse dellstore_to_clickhouse 2023-01-01
```

activate inactive job
```bash
$ airflow dags unpause dellstore_to_clickhouse
```

#### Demo

![demo](./task_17.gif)