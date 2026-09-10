## Sharding in ClickHouse

1. Configuration 1 shard 2 replicas

```xml
<clickhouse replace="true">
    <logger>
        <level>debug</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>1000M</size>
        <count>3</count>
    </logger>
    <display_name>clickhouse-01</display_name>
    <listen_host>0.0.0.0</listen_host>
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>
    <user_directories>
        <users_xml>
            <path>users.xml</path>
        </users_xml>
        <local_directory>
            <path>/var/lib/clickhouse/access/</path>
        </local_directory>
    </user_directories>
    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
    </distributed_ddl>
    <remote_servers >
        <cluster_1S_2R>
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                </replica>
            </shard>
        </cluster_1S_2R>
    </remote_servers>
    <zookeeper>
        <node>
            <host>clickhouse-keeper</host>
            <port>9181</port>
        </node>
    </zookeeper>
    <macros>
        <shard>01</shard>
        <replica>01</replica>
        <cluster>cluster_1S_2R</cluster>
    </macros>
</clickhouse>
```

2. Configuration 2 shards 2 replicas

```xml
<clickhouse replace="true">
    <logger>
        <level>debug</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>1000M</size>
        <count>3</count>
    </logger>
    <display_name>cluster_2S_2R node 1</display_name>
    <listen_host>0.0.0.0</listen_host>
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>
    <user_directories>
        <users_xml>
            <path>users.xml</path>
        </users_xml>
        <local_directory>
            <path>/var/lib/clickhouse/access/</path>
        </local_directory>
    </user_directories>
    <distributed_ddl>
        <path>/clickhouse/task_queue/ddl</path>
    </distributed_ddl>
    <remote_servers>
        <cluster_2S_2R>
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-01</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-03</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-02</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-04</host>
                    <port>9000</port>
                </replica>
            </shard>
        </cluster_2S_2R>
    </remote_servers>
    <zookeeper>
        <node>
            <host>clickhouse-keeper</host>
            <port>9181</port>
        </node>
    </zookeeper>
    <macros>
        <shard>01</shard>
        <replica>01</replica>
        <cluster>cluster_2S_2R</cluster>
    </macros>
</clickhouse>
```

### Docker-compose file

[../../docker-compose.s]()

local table

```sql
CREATE TABLE trips_local ON CLUSTER '{cluster}' 
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/trips_local', '{replica}')
ORDER BY pickup_date
AS 
SELECT * FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{0..2}.gz', 
    'TabSeparatedWithNames'
) LIMIT 0
SETTINGS schema_inference_make_columns_nullable = 0;
```

distributed table

```sql
CREATE TABLE trips_distributed ON CLUSTER 'cluster_2S_2R' 
AS default.trips_local
ENGINE = Distributed(
    'cluster_2S_2R',
    'default',
    'trips_local',
    rand()
);
```

input data

```sql
INSERT INTO default.trips_distributed
SELECT * FROM s3(
    'https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/trips_{0..2}.gz', 
    'TabSeparatedWithNames'
);
```

#### Demo

![demo](./task_11.gif)
