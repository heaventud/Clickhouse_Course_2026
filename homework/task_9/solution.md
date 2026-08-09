## Projections and Materialized Views in Clickhouse

-- Test [`sales` table DDL](../../migrations/09_migration.sql)

Create a projection to sum sales by product.
```sql
ALTER TABLE sales ADD PROJECTION IF NOT EXISTS product_sales_projection 
(
    SELECT product_id,
        sum(quantity) as total_quantity,
        sum(price * quantity) as total_sales
    GROUP BY product_id
);

ALTER TABLE sales MATERIALIZE PROJECTION IF EXISTS product_sales_projection;

```

Create a target table for materialized view
```sql
CREATE TABLE IF NOT EXISTS product_sales (
    product_id UInt32,
    total_quantity UInt64,
    total_sales Float64,
    last_update DateTime DEFAULT now64(3)
) ENGINE = MergeTree() 
ORDER BY last_update
;
```

Create a materialized view to keep aggregation data
```sql
CREATE MATERIALIZED VIEW IF NOT EXISTS product_sales_mv TO product_sales 
AS 
SELECT 
    product_id,
    sum(quantity) as total_quantity,
    sum(price * quantity) as total_sales
FROM sales 
GROUP BY product_id
;
```

Insert new data into `sales` table
```sql
INSERT INTO sales
SELECT
    number + 1 AS id,
    (cityHash64(number * 31) % 500) + 1 AS product_id,
    (cityHash64(number * 43) % 5) + 1 AS quantity,
    round(((cityHash64(number * 59) % 100000) / 100.0) + 10, 2) AS price,
    today() - (cityHash64(number * 71) % 365) AS sale_date
FROM numbers()
LIMIT 20000 OFFSET 10000
;
```

Find data using projections
```sql
EXPLAIN plan
SELECT
    product_id,
    sum(quantity) AS total_quantity,
    CAST(sum(price * quantity) AS Decimal(10,2)) AS total_sales
FROM sales
GROUP BY product_id
;
```

Find data in target table
```sql
SELECT
    product_id,
    total_quantity,
    CAST(total_sales AS Decimal(10,2)) AS total_sales
FROM product_sales
;
```

```sql
ALTER TABLE sales ADD PROJECTION IF NOT EXISTS sales_by_month_projection 
(
    SELECT
        toStartOfMonth(sale_date) as month,
        sum(quantity) as total_quantity,
        sum(price * quantity) as total_sales
    GROUP BY month
);

SELECT
    toStartOfMonth(sale_date) as month,
    sum(quantity) as total_quantity,
    sum(price * quantity) as total_sales
FROM sales
GROUP BY month;

ALTER TABLE sales MATERIALIZE PROJECTION IF EXISTS sales_by_month_projection;
```

Console demonstration:
![demo](task_9.gif)