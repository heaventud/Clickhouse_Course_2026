CREATE TABLE sales
(
    id UInt32 COMMENT 'unique id',
    product_id UInt32 COMMENT 'product id',
    quantity UInt32 COMMENT 'number of units sold',
    price Float32 COMMENT 'price per unit',
    sale_date DateTime COMMENT 'date of sale'
)
ENGINE = MergeTree()
ORDER BY (id, sale_date);

INSERT INTO sales
SELECT
    number + 1 AS id,
    (cityHash64(number * 31) % 500) + 1 AS product_id,
    (cityHash64(number * 43) % 5) + 1 AS quantity,
    round(((cityHash64(number * 59) % 100000) / 100.0) + 10, 2) AS price,
    today() - (cityHash64(number * 71) % 365) AS sale_date
FROM numbers(10000);
