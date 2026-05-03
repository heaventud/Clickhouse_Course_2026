CREATE DATABASE commertial_db;

CREATE TABLE commertial_db.transactions (
    transaction_id UInt32,
    user_id UInt32,
    product_id UInt32,
    quantity UInt8,
    price Float32,
    transaction_date Date
) ENGINE = MergeTree()
ORDER BY (transaction_id);

INSERT INTO commertial_db.transactions
SELECT
    number + 1 AS transaction_id,
    (cityHash64(number * 17) % 1000) + 1 AS user_id,
    (cityHash64(number * 31) % 500) + 1 AS product_id,
    (cityHash64(number * 43) % 5) + 1 AS quantity,
    round(((cityHash64(number * 59) % 100000) / 100.0) + 10, 2) AS price,
    today() - (cityHash64(number * 71) % 365) AS transaction_date
FROM numbers(10000);
