### Purpose
 - To prepare clickhouse instance with an basic configuration, measure performance with/without optimizations. 

### Instructions
- Install ClickHouse.
- Load the test dataset and run a query against the table.
- Submit screenshots of the running ClickHouse instance, the created virtual machine (if you are completing the task in Yandex Cloud), and the result of the query `select count() from trips where payment_type = 1`.
- Perform performance testing and save the results.
- Study the database configuration files.
- Tune the system according to your OS characteristics, optimize the parameters, and run the performance tests again.
- Prepare a report on the performance increase/change based on the applied tuning. Clearly specify which parameters were changed and why.

### Demo

![Terminal demo](./term_1.gif)

### Benchmark Profiles

`clickhouse_users/test_profiles.xml` defines two settings profiles used for benchmarking:
- `baseline`: `max_threads=1`, `max_memory_usage=2147483648`, `use_uncompressed_cache=0`
- `optimized`: `max_threads=4`, `max_memory_usage=6442450944`, `use_uncompressed_cache=1`

`clickhouse_users/test_users.xml` binds benchmark users to these profiles:
- `baseline_user` -> `baseline`
- `optimized_user` -> `optimized`

### Benchmark Commands

Run the baseline profile benchmark:

```bash
docker exec clickhouse clickhouse-benchmark -c 3 -t 60 -d 0 \
  --user baseline_user \
  --password baseline_pass \
  --query "SELECT count() FROM taxi.trips WHERE payment_type = 1"
```

Run the optimized profile benchmark:

```bash
docker exec clickhouse clickhouse-benchmark -c 3 -t 60 -d 0 \
  --user optimized_user \
  --password optimized_pass \
  --query "SELECT count() FROM taxi.trips WHERE payment_type = 1"
```

### Benchmark Results

| User | Queries executed | QPS | Median (p50) | p95 |
|---|---:|---:|---:|---:|
| `baseline_user` | 12523 | 208.673 | 0.011 s | 0.023 s |
| `optimized_user` | 12887 | 214.307 | 0.010 s | 0.022 s |


