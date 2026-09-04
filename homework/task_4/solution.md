## SQL in ClickHouse

1.
```sql
CREATE DATABASE IF NOT EXISTS restaurant;
       
CREATE TABLE restaurant.dish_menu (
    id UInt32 COMMENT 'Unique identifier',
    name LowCardinality(String) COMMENT 'Name of the dish',
    price Decimal(10,2) DEFAULT 0 COMMENT 'Price of the dish',
    ingredients String COMMENT 'Ingredients of the dish',
    is_vegan Bool DEFAULT false COMMENT 'Is the dish vegan',
    is_available Bool COMMENT 'Is the dish available',
    created_at DateTime DEFAULT now() COMMENT  'Date when row was created',
    updated_at DateTime DEFAULT now() COMMENT 'Date when row was updated'
) ENGINE = MergeTree() 
ORDER BY id
SETTINGS index_granularity = 8192
;
```

2.
--- test data ---
```sql
INSERT INTO TABLE restaurant.dish_menu
    (id, name, price, ingredients, is_vegan, is_available)
VALUES (1, 'Cheeseburger', 10.50, 'Parmezan,latuc,tomato,onion,beef party,buns', false, true),
       (2, 'Margarita Pizza', 12.50, 'pepperoni,mushrooms,onion,tomato,olives,pineapple,bacon', true, true)
;

SELECT * FROM restaurant.dish_menu
WHERE price >= 10.00;

ALTER TABLE restaurant.dish_menu UPDATE price = 15.86, updated_at=now() WHERE name = 'Cheeseburger';

DELETE FROM restaurant.dish_menu WHERE name = 'Cheeseburger';

```

```sql
ALTER TABLE restaurant.dish_menu ADD COLUMN is_spicy Bool DEFAULT false;
ALTER TABLE restaurant.dish_menu MODIFY COLUMN is_spicy COMMENT 'Is the dish spicy';
ALTER TABLE restaurant.dish_menu DROP COLUMN is_vegan;
```


3. Materialize a table

```sql
CREATE TABLE taxi_trips_mat AS taxi.trips;

SELECT
    partition,
    partition_id,
    count()
FROM system.parts
WHERE `table` = 'trips' AND active
GROUP BY
    partition,
    partition_id
;

ALTER TABLE taxi_trips_mat 
REPLACE PARTITION tuple() FROM taxi.trips
;
```
