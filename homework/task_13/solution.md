## RBAC in Clickhouse


#### Create test user 
```sql
-- Create a new user
CREATE USER IF NOT EXISTS jhon
IDENTIFIED WITH plaintext_password BY 'qwerty' 
DEFAULT DATABASE taxi
;
SELECT *
FROM system.users
WHERE name ILIKE 'jhon'
;
-- Create a new role
CREATE ROLE IF NOT EXISTS devs
;
GRANT SELECT ON taxi.* TO devs;
SELECT *
FROM system.roles
WHERE name ILIKE 'devs'
;
-- Grant role to user
GRANT devs TO jhon
;
SELECT *
FROM system.grants
WHERE user_name = 'jhon'
;
SELECT count(1)
FROM taxi.trips
WHERE trip_amount > 100
;
```

#### Demo

![Terminal](./task_13.gif)
