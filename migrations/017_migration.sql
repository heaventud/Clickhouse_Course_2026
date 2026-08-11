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