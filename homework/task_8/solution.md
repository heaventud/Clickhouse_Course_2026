## Task 8: Clickhouse Dictionaries


#### Prepare Data

```sql
CREATE TABLE default.transactions (
    user_id UInt64,
    action LowCardinality(String),
    expense UInt64,
    timestamp TIMESTAMP
)
ENGINE = MergeTree()
ORDER BY user_id
;

CREATE DICTIONARY IF NOT EXISTS default.user_dict (
    user_id UInt64,
    email String
)
PRIMARY KEY user_id
SOURCE(FILE(path '/var/lib/clickhouse/user_files/dict_data.csv' format 'CSV'))
LAYOUT(HASHED())
LIFETIME(MIN 0 MAX 0)
;


INSERT INTO default.transactions
SELECT
    user_id,
    action,
    expense,
    toDateTime(ts) AS timestamp
FROM file(
    'table_data.txt',
    'Values',
    'user_id UInt64, action String, expense UInt64, ts Float64'
);
```

#### Query to find cumulative expense of the top 10 users by action type

```sql
with top_10_by_action as (
    select *
    from default.transactions
    order by action, expense desc
    limit 10 by action
)
select
    dictGet('user_dict', 'email', user_id) as user_email,
    action,
    sum(expense) over(partition by action order by user_email) as cum_expenses
from top_10_by_action
;
```


#### Demo

![Terminal](./task_8.gif)
