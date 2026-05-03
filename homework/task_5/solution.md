## Task 1

--- test data ---
```sql
INSERT INTO commertial_db.transactions
SELECT
    number + 1 AS transaction_id,
    (cityHash64(number * 17) % 1000) + 1 AS user_id,
    (cityHash64(number * 31) % 500) + 1 AS product_id,
    (cityHash64(number * 43) % 5) + 1 AS quantity,
    round(((cityHash64(number * 59) % 100000) / 100.0) + 10, 2) AS price,
    today() - (cityHash64(number * 71) % 365) AS transaction_date
FROM numbers(10000)
;
```

1.
```sql
WITH uniq_tr AS
    (
        SELECT
            transaction_id,
            anyLast(user_id) AS user_id,
            anyLast(price) AS price,
            anyLast(quantity) AS quantity
        FROM transactions
        GROUP BY transaction_id
    )
SELECT
    sum(price * quantity) AS total_sum,
    avg(price * quantity) AS avg_profit,
    sum(quantity) AS total_quantity,
    countDistinct(user_id) AS cnt_customers
FROM uniq_tr
;
```

   ┌──────────total_sum─┬─────────avg_profit─┬─total_quantity─┬─cnt_customers─┐
   │ 15450420.989207268 │ 1545.0420989207269 │          30087 │          1000 │
   └────────────────────┴────────────────────┴────────────────┴───────────────┘
2.
```bash
SELECT formatDateTime(transaction_date, '%Y-%m-%d') AS transaction_date
FROM transactions
LIMIT 1

Query id: 7f5d2050-0034-47ff-a2b3-99bb04b0207a

   ┌─transaction_date─┐
1. │ 2026-02-27       │
   └──────────────────┘
```

```bash
SELECT
    toMonth(transaction_date) AS transaction_month,
    toYear(transaction_date) AS transaction_year
FROM transactions
LIMIT 1

Query id: e5729fe7-b8eb-4587-b7b2-c0cf69ff5d64

   ┌─transaction_month─┬─transaction_year─┐
1. │                 2 │             2026 │
   └───────────────────┴──────────────────┘
```

```bash
WITH uniq_tr AS
    (
        SELECT
            transaction_id,
            anyLast(user_id) AS user_id,
            anyLast(price) AS price,
            anyLast(quantity) AS quantity
        FROM transactions
        GROUP BY transaction_id
    )
SELECT toInt32(sum(price * quantity)) AS total_sum
FROM uniq_tr

Query id: b1ce1929-c0ee-4e3d-a324-1205f3e0ba88

   ┌─total_sum─┐
1. │  15450420 │ -- 15.45 million
   └───────────┘

```

```bash
SELECT
    price,
    toString(price) AS price_as_str,
    toTypeName(price_as_str)
FROM transactions
LIMIT 1

Query id: 2c1c939f-5c33-4956-bcde-42e6d7da377b

   ┌─price─┬─price_as_str─┬─toTypeName(price_as_str)─┐
1. │ 148.1 │ 148.1        │ String                   │
   └───────┴──────────────┴──────────────────────────┘

```

```bash
SELECT *
FROM system.functions
WHERE name = 'total_profit'

Query id: a74191d5-762f-4e72-bf71-5789d18734eb

   ┌─name─────────┬─is_aggregate─┬─case_insensitive─┬─alias_to─┬─create_query──────────────────────────────────────────────────────────┬─origin─────────┬─description─┬─syntax─┬─arguments─┬─parameters─┬─returned_value─┬─examples─┬─introduced_in─┬─categories─┐
1. │ total_profit │            0 │                0 │          │ CREATE FUNCTION total_profit AS (qnt, price) -> floor(qnt * price, 2) │ SQLUserDefined │             │        │           │            │                │          │               │            │
   └──────────────┴──────────────┴──────────────────┴──────────┴───────────────────────────────────────────────────────────────────────┴────────────────┴─────────────┴────────┴───────────┴────────────┴────────────────┴──────────┴───────────────┴────────────┘
```

```bash
SELECT total_profit(quantity, price) AS profit
FROM transactions
ORDER BY profit DESC
LIMIT 3

Query id: 756af2a0-1a3f-4f4c-b3fe-e6cb93ab8e06

   ┌──profit─┐
1. │ 5048.04 │
2. │ 5046.84 │
3. │    5042 │
   └─────────┘
```

```bash

SELECT *
FROM system.functions
WHERE name = 'what_price_str'

Query id: df969c8f-35f4-4ec2-9fd2-5cbfee779c28

   ┌─name───────────┬─is_aggregate─┬─case_insensitive─┬─alias_to─┬─create_query─────────────────────────────────────────────────────────────────────────────────────────────┬─origin─────────┬─description─┬─syntax─┬─arguments─┬─parameters─┬─returned_value─┬─examples─┬─introduced_in─┬─categories─┐
1. │ what_price_str │            0 │                0 │          │ CREATE FUNCTION what_price_str AS (cost, threashold) -> if(cost > threashold, 'high_price', 'low_price') │ SQLUserDefined │             │        │           │            │                │          │               │            │
   └────────────────┴──────────────┴──────────────────┴──────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────┴─────────────┴────────┴───────────┴────────────┴────────────────┴──────────┴───────────────┴────────────┘
```

```bash
SELECT what_price_str(price, 1000)
FROM transactions
WHERE (price > 900) AND (price < 1100)
LIMIT 3

Query id: e1b0e3d1-baa2-4ff8-ab79-cd52502f59fe

   ┌─what_price_str(price, 1000)─┐
1. │ high_price                  │
2. │ low_price                   │
3. │ low_price                   │
   └─────────────────────────────┘
```

## Task 2

#### Preparing actions
```bash
root@e740c77aac3e:/# apt-get update
root@e740c77aac3e:/# apt-get install -y python3 python3-pip
root@e740c77aac3e:/# which python3
/usr/bin/python3
root@e740c77aac3e:/# 
```