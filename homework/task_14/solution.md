## Backup for Clickhouse

#### Use S3 as a backup storage
[Clickhouse configuration ](./config.xml)

#### Check connection to S3
```bash
clickhouse-client -m "
INSERT INTO FUNCTION
   s3(
       'http://s3:10000/clickhouse/csv/trips.csv.lz4',
       'clickhouse',
       'clickhouse_secret',
       'CSV'
    )
SELECT *
FROM taxi.trips
LIMIT 10000;"
```

#### Configure `clickhouse-backup` to use S3 as a backup storage
[backup-config.yml](./clickhouse-backup-config.yml)

```bash
mv ./clickhouse-backup-config.yml /etc/clickhouse-backup/config.yml
```


#### Backup `taxi` database on remote S3 server
```bash
clickhouse-backup create_remote backup_taxi_db_remote -t 'taxi.*'
```

#### Drop table taxi.trips
```bash
clickhouse-client -m '
DROP TABLE IF EXISTS taxi.trips SYNC;
SELECT *
FROM taxi.trips
LIMIT 1
FORMAT vertical;
'
```

#### Restore table taxi.trips from remote S3 server
```bash
clickhouse-backup list remote 2>&1 | grep backup_taxi_db_remote
clickhouse-backup restore_remote backup_taxi_db_remote -t 'taxi.*' 
```

#### Check restored table taxi.trips
```bash
clickhouse-client -m '
SELECT *
FROM taxi.trips
LIMIT 1
FORMAT vertical;
'
```

### Demo
![demo](./task_14.gif)
