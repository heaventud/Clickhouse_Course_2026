## Mutations, partitions, parts in Clickhouse


#### prepare test data in Clickhouse
[fake_data_generator.py](./fake_data_generation.py)

```bash
python homework/task_12/fake_data_generation.py | \
docker exec -i clickhouse clickhouse-client                            /1.5s
```

```sql
SELECT count()
FROM user_activity;

SELECT countDistinct(partition)
FROM system.parts
WHERE `table` = 'user_activity' AND active
;

SELECT concat(
    'ALTER TABLE user_activity ',
    'UPDATE activity_type = ''pay'' ',
    'IN PARTITION ',
    partition_id,
    ' WHERE activity_type = ''purchase'';'
) AS update_sql
FROM
(
    SELECT DISTINCT partition_id
    FROM system.parts
    WHERE database = 'default'
      AND table = 'user_activity'
      AND active
    ORDER BY partition_id
)
;

select count() from system.mutations where table = 'user_activity';

ALTER TABLE user_activity DROP PARTITION '202607';

SELECT count() from system.mutations where table = 'user_activity';

SELECT 
    partition,
    name,
    part_type,
    active,
    visible,
    bytes_on_disk,
    data_compressed_bytes,
    marks_bytes,
    rows
FROM system.parts 
WHERE table = 'user_activity' AND partition_id = '202607'
FORMAT VERTICAL
;

SELECT count() from user_activity WHERE toStartOfMonth(activity_date) = '2026-07-01';
```

### Demo
![demo](./task_12.gif)
