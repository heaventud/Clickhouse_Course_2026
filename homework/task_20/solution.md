## Clickhouse/PostgreSQL integration

Credentials in named collection in clickhouse to integrate with Postgres

```xml
<clickhouse>
    <named_collections>
        <pgdata>
            <user>baseline_user</user>
            <password>baseline_pass</password>
            <host>postgres</host>
            <port>5432</port>
            <database>dellstore</database>
            <schema>public</schema>
        </pgdata>
    </named_collections>
</clickhouse>
```


1. Read data from postgres using a built-in function

```sql
SELECT *
FROM postgresql(pgdata, `table` = 'products')
LIMIT 10;
```

2. Create replica table in clickhouse

```sql
CREATE TABLE IF NOT EXISTS pg_products (
    prod_id Int32,
    category Int32,
    title String,
    actor String,
    price Decimal(12, 2),
    special Int16,
    common_prod_id Int32
)
ENGINE = PostgreSQL(pgdata, table='products');
```

3. Create replication database in clickhouse

#### Adjust Postgres server

a. Create user and grant permissions for valid replication

```sql
CREATE ROLE baseline_user WITH LOGIN PASSWORD 'baseline_pass' REPLICATION;

GRANT CONNECT ON DATABASE dellstore TO baseline_user;
GRANT USAGE ON SCHEMA public TO baseline_user;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO baseline_user;
```

2.Adjust Postgres server

a. Create user and grant permissions for valid replication

```sql
CREATE ROLE baseline_user WITH LOGIN PASSWORD 'baseline_pass' REPLICATION;

GRANT CONNECT ON DATABASE dellstore TO baseline_user;
GRANT USAGE ON SCHEMA public TO baseline_user;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO baseline_user;
```

b. Check connection for clickhouse user

```bash
$ psql -U baseline_user -d dellstore -W
```

c. Set WAL level to logical

```sql
ALTER SYSTEM SET wal_level = 'logical';
```

d. Create database with replication in clickhouse
```sql
CREATE DATABASE pg_db
ENGINE = MaterializedPostgreSQL(pgdata)
SETTINGS materialized_postgresql_tables_list = 'products,categories,orders'
;
```

![demo](./task_20.gif)

