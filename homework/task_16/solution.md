## Query Profiling in ClickHouse

1. Query uses a primary key.

```sql
SELECT
    pickup_ntaname,
    count() AS trips_count,
    avg(fare_amount) AS avg_fare
FROM trips
WHERE (pickup_datetime >= '2015-07-01 00:00:00') AND (pickup_datetime < '2015-09-01 00:00:00')
GROUP BY pickup_ntaname
ORDER BY trips_count DESC
SETTINGS send_logs_level = 'trace'
;
```

```text
Query id: e21bf87a-8619-4c1f-8b11-c2ae5c42282f

[clickhouse] 2026.09.07 20:03:27.089629 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> executeQuery: (from 127.0.0.1:54714) (query 1, line 1) SELECT pickup_ntaname, count() AS trips_count, avg(fare_amount) AS avg_fare FROM trips WHERE (pickup_datetime >= '2015-07-01 00:00:00') AND (pickup_datetime < '2015-09-01 00:00:00') GROUP BY pickup_ntaname ORDER BY trips_count DESC SETTINGS send_logs_level = 'trace' ; (stage: Complete)
[clickhouse] 2026.09.07 20:03:27.090221 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Planner: Query to stage Complete
[clickhouse] 2026.09.07 20:03:27.090360 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Planner: Query from stage FetchColumns to stage Complete
[clickhouse] 2026.09.07 20:03:27.090552 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Adjusting memory limit before external aggregation with 2.96 GiB (ratio: 0.5, available system memory: 5.92 GiB)
[clickhouse] 2026.09.07 20:03:27.090610 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> SortingStep: Adjusting memory limit before external sort with 2.96 GiB (ratio: 0.5, available system memory: 5.92 GiB)
[clickhouse] 2026.09.07 20:03:27.090863 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> QueryPlanOptimizePrewhere: The min valid primary key position for moving to the tail of PREWHERE is 0
[clickhouse] 2026.09.07 20:03:27.090901 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> QueryPlanOptimizePrewhere: Moved 2 conditions to PREWHERE
[clickhouse] 2026.09.07 20:03:27.091036 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> IInterpreterUnionOrSelectQuery: The analyzer is enabled, but the old interpreter is used. It can be a bug, please report it. Will disable 'allow_experimental_analyzer' setting (for query: SELECT min(pickup_datetime), max(pickup_datetime), count() SETTINGS aggregate_functions_null_for_empty = false, transform_null_in = false, legacy_column_name_of_tuple_literal = false)
[clickhouse] 2026.09.07 20:03:27.091295 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Key condition: (column 0 in [1435708800, +Inf)), (column 0 in (-Inf, 1441065599]), and
[clickhouse] 2026.09.07 20:03:27.091348 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Query condition cache has dropped 0/368 granules for PREWHERE condition and(greaterOrEquals(__table1.pickup_datetime, '2015-07-01 00:00:00'_String), less(__table1.pickup_datetime, '2015-09-01 00:00:00'_String)).
[clickhouse] 2026.09.07 20:03:27.091369 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Query condition cache has dropped 93/368 granules for WHERE condition and(greaterOrEquals(pickup_datetime, '2015-07-01 00:00:00'_String), less(pickup_datetime, '2015-09-01 00:00:00'_String)).
[clickhouse] 2026.09.07 20:03:27.091378 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Filtering marks by primary and secondary keys
[clickhouse] 2026.09.07 20:03:27.091391 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Running binary search on index range for part all_1_3_1 (369 marks)
[clickhouse] 2026.09.07 20:03:27.091432 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Found (LEFT) boundary mark: 0
[clickhouse] 2026.09.07 20:03:27.091449 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Found (RIGHT) boundary mark: 275
[clickhouse] 2026.09.07 20:03:27.091456 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Found continuous range in 17 steps
[clickhouse] 2026.09.07 20:03:27.091468 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): PK index has dropped 93/368 granules, it took 0ms across 1 threads.
[clickhouse] 2026.09.07 20:03:27.091490 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Selected 1/1 parts by partition key, 1 parts by primary key, 275/368 marks by primary key, 275 marks to read from 1 ranges
[clickhouse] 2026.09.07 20:03:27.091525 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Spreading mark ranges among streams (default reading)
[clickhouse] 2026.09.07 20:03:27.091602 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Reading approx. 2251085 rows with 8 streams
[clickhouse] 2026.09.07 20:03:27.093467 [ 794 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.093575 [ 829 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.093648 [ 829 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.093662 [ 829 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.093677 [ 902 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.093688 [ 902 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.093698 [ 902 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.093923 [ 890 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.093937 [ 890 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.093944 [ 890 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.094149 [ 938 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.094160 [ 938 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.094165 [ 938 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.094202 [ 949 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.094217 [ 949 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.094224 [ 949 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.094369 [ 944 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.094378 [ 944 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.094384 [ 944 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.094448 [ 922 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:03:27.094457 [ 922 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.094465 [ 922 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.096038 [ 794 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> HashTablesStatistics: An entry for key=9034814189045997479 found in cache: sum_of_sizes=1326, median_size=168
[clickhouse] 2026.09.07 20:03:27.096060 [ 794 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:03:27.096556 [ 829 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 162 rows (from 1.37 MiB) in 0.004696167 sec. (61054046.843 rows/sec., 291.13 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097289 [ 902 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 163 rows (from 1.37 MiB) in 0.005427416 sec. (52828086.146 rows/sec., 251.90 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097290 [ 922 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 242038 to 162 rows (from 1.15 MiB) in 0.005419167 sec. (44663321.872 rows/sec., 212.97 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097626 [ 949 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 168 rows (from 1.37 MiB) in 0.005765625 sec. (49729214.092 rows/sec., 237.13 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097628 [ 890 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 170 rows (from 1.37 MiB) in 0.005767583 sec. (49712331.838 rows/sec., 237.05 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097829 [ 938 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 164 rows (from 1.37 MiB) in 0.005964209 sec. (48073432.705 rows/sec., 229.23 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.097942 [ 944 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 168 rows (from 1.37 MiB) in 0.006076584 sec. (47184404.922 rows/sec., 224.99 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.098882 [ 794 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> AggregatingTransform: Aggregated. 286720 to 169 rows (from 1.37 MiB) in 0.007033292 sec. (40766116.351 rows/sec., 194.39 MiB/sec.)
[clickhouse] 2026.09.07 20:03:27.098918 [ 794 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Trace> Aggregator: Merging aggregated data
[clickhouse] 2026.09.07 20:03:27.099915 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> executeQuery: Read 2251085 rows, 19.32 MiB in 0.010391 sec., 216637955.92339528 rows/sec., 1.82 GiB/sec.
[clickhouse] 2026.09.07 20:03:27.099977 [ 87 ] {e21bf87a-8619-4c1f-8b11-c2ae5c42282f} <Debug> MemoryTracker: Query peak memory usage: 9.46 MiB.
```

2. Query does not use a primary key.

```sql
SELECT 
    pickup_ntaname, 
    count() AS trips_count, 
    avg(fare_amount) AS avg_fare
FROM taxi.trips
WHERE passenger_count = 4
GROUP BY pickup_ntaname
ORDER BY trips_count DESC
SETTINGS send_logs_level = 'trace'
;
```

```text
[clickhouse] 2026.09.07 20:02:00.420756 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> executeQuery: (from 127.0.0.1:54714) (query 1, line 1) SELECT pickup_ntaname, count() AS trips_count, avg(fare_amount) AS avg_fare FROM taxi.trips WHERE passenger_count = 4 GROUP BY pickup_ntaname ORDER BY trips_count DESC SETTINGS send_logs_level = 'trace' ; (stage: Complete)
[clickhouse] 2026.09.07 20:02:00.421399 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Planner: Query to stage Complete
[clickhouse] 2026.09.07 20:02:00.421735 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Planner: Query from stage FetchColumns to stage Complete
[clickhouse] 2026.09.07 20:02:00.421905 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Adjusting memory limit before external aggregation with 2.97 GiB (ratio: 0.5, available system memory: 5.94 GiB)
[clickhouse] 2026.09.07 20:02:00.422034 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> SortingStep: Adjusting memory limit before external sort with 2.97 GiB (ratio: 0.5, available system memory: 5.94 GiB)
[clickhouse] 2026.09.07 20:02:00.422277 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> QueryPlanOptimizePrewhere: The min valid primary key position for moving to the tail of PREWHERE is -1
[clickhouse] 2026.09.07 20:02:00.422377 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> QueryPlanOptimizePrewhere: Moved 1 conditions to PREWHERE
[clickhouse] 2026.09.07 20:02:00.422508 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> IInterpreterUnionOrSelectQuery: The analyzer is enabled, but the old interpreter is used. It can be a bug, please report it. Will disable 'allow_experimental_analyzer' setting (for query: SELECT min(pickup_datetime), max(pickup_datetime), count() SETTINGS aggregate_functions_null_for_empty = false, transform_null_in = false, legacy_column_name_of_tuple_literal = false)
[clickhouse] 2026.09.07 20:02:00.422852 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Key condition: unknown
[clickhouse] 2026.09.07 20:02:00.422976 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Query condition cache has dropped 0/368 granules for PREWHERE condition equals(__table1.passenger_count, 4_UInt8).
[clickhouse] 2026.09.07 20:02:00.422992 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Query condition cache has dropped 0/368 granules for WHERE condition equals(passenger_count, 4_UInt8).
[clickhouse] 2026.09.07 20:02:00.423007 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Filtering marks by primary and secondary keys
[clickhouse] 2026.09.07 20:02:00.423018 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): PK index has dropped 0/368 granules, it took 0ms across 1 threads.
[clickhouse] 2026.09.07 20:02:00.423041 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Selected 1/1 parts by partition key, 1 parts by primary key, 368/368 marks by primary key, 368 marks to read from 1 ranges
[clickhouse] 2026.09.07 20:02:00.423066 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Spreading mark ranges among streams (default reading)
[clickhouse] 2026.09.07 20:02:00.423141 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> taxi.trips (3ab07f96-6353-4ce3-9924-b30bab714434) (SelectExecutor): Reading approx. 3000317 rows with 8 streams
[clickhouse] 2026.09.07 20:02:00.425442 [ 930 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.425481 [ 930 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.425493 [ 980 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.425496 [ 930 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.425520 [ 980 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.425533 [ 980 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.425598 [ 932 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.425612 [ 932 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.425623 [ 932 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.425667 [ 750 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.425688 [ 750 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.425701 [ 750 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.425810 [ 971 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.425818 [ 971 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.425829 [ 971 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.426225 [ 946 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.426425 [ 946 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.426437 [ 946 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.426731 [ 927 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.426825 [ 936 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregating
[clickhouse] 2026.09.07 20:02:00.426840 [ 927 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.426946 [ 936 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> HashTablesStatistics: An entry for key=13871935311221433248 found in cache: sum_of_sizes=586, median_size=76
[clickhouse] 2026.09.07 20:02:00.426964 [ 936 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.427052 [ 927 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Aggregation method: low_cardinality_key_string
[clickhouse] 2026.09.07 20:02:00.428935 [ 936 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 4138 to 67 rows (from 20.21 KiB) in 0.0054915 sec. (753528.180 rows/sec., 3.59 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.429222 [ 932 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 8936 to 74 rows (from 43.63 KiB) in 0.005805042 sec. (1539351.481 rows/sec., 7.34 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.429256 [ 930 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 8405 to 79 rows (from 41.04 KiB) in 0.005834541 sec. (1440558.906 rows/sec., 6.87 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.429588 [ 750 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 8873 to 70 rows (from 43.33 KiB) in 0.006174042 sec. (1437146.038 rows/sec., 6.85 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.429858 [ 971 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 7833 to 65 rows (from 38.25 KiB) in 0.006437625 sec. (1216753.073 rows/sec., 5.80 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.430038 [ 927 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 7144 to 71 rows (from 34.88 KiB) in 0.00660925 sec. (1080909.332 rows/sec., 5.15 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.430049 [ 946 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 8564 to 76 rows (from 41.82 KiB) in 0.006640583 sec. (1289645.804 rows/sec., 6.15 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.430471 [ 980 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> AggregatingTransform: Aggregated. 12115 to 84 rows (from 59.16 KiB) in 0.00705675 sec. (1716795.975 rows/sec., 8.19 MiB/sec.)
[clickhouse] 2026.09.07 20:02:00.430490 [ 980 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Trace> Aggregator: Merging aggregated data
[clickhouse] 2026.09.07 20:02:00.431449 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> executeQuery: Read 3000317 rows, 17.17 MiB in 0.010864 sec., 276170563.32842416 rows/sec., 1.54 GiB/sec.
[clickhouse] 2026.09.07 20:02:00.431552 [ 87 ] {4e589f53-fc07-4a50-9f5a-be9c4595d056} <Debug> MemoryTracker: Query peak memory usage: 6.09 MiB.
```

#### Queries Analyzing

```sql
EXPLAIN indexes = 1
SELECT count() 
FROM trips 
WHERE (pickup_datetime >= '2015-07-01 00:00:00') 
  AND (pickup_datetime < '2015-09-01 00:00:00')
;
```

```sql
EXPLAIN indexes = 1
SELECT 
    pickup_ntaname, 
    count() AS trips_count, 
    avg(fare_amount) AS avg_fare
FROM taxi.trips
WHERE passenger_count = 4
GROUP BY pickup_ntaname
ORDER BY trips_count DESC
;
```

![demo](./task_16.gif)
