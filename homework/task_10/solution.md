## Tables replication in Clickhouse

the replicated table
```sql
CREATE DATABASE IF NOT EXISTS taxi;

CREATE TABLE taxi.trips (
    trip_id             UInt32,
    pickup_datetime     DateTime,
    dropoff_datetime    DateTime,
    pickup_longitude    Nullable(Float64),
    pickup_latitude     Nullable(Float64),
    dropoff_longitude   Nullable(Float64),
    dropoff_latitude    Nullable(Float64),
    passenger_count     UInt8,
    trip_distance       Float32,
    fare_amount         Float32,
    extra               Float32,
    tip_amount          Float32,
    tolls_amount        Float32,
    total_amount        Float32,
    payment_type        Enum('CSH' = 1, 'CRE' = 2, 'NOC' = 3, 'DIS' = 4, 'UNK' = 5),
    pickup_ntaname      LowCardinality(String),
    dropoff_ntaname     LowCardinality(String),
    date                Date DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{table}', '{replica}')
PRIMARY KEY (pickup_datetime, dropoff_datetime)
ORDER BY (pickup_datetime, dropoff_datetime)
TTL date + INTERVAL 7 DAY DELETE;

INSERT INTO taxi.trips
SELECT *
FROM gcs(
    'https://storage.googleapis.com/clickhouse-public-datasets/nyc-taxi/trips_{0..2}.gz',
    'TabSeparatedWithNames'
);
```

#### Result file

```bash
docker exec -it clickhouse-02 clickhouse-client  --query "
SELECT                   
getMacro('replica'),
*
FROM remote('clickhouse-01,clickhouse-02', system.parts)
FORMAT JSONEachRow;
" > file.json
```

[file.json]()

#### Demo

![demo](task_10.gif)
