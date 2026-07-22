## Use Kafka integration in Clickhouse

#### Create a test kafka topic
```bash
/bin/kafka-topics --create \
    --if-not-exists \
    --bootstrap-server "kafka1:9092" \
    --topic "kafka-topic-2" \
    --partitions 1 \
    --replication-factor 1
```

#### Create a test table and materialized view in clickhouse
```sql
CREATE TABLE kafka_queue
(
    event_id UInt16,
    key String,
    value String,
    comment Nullable(String)
)
ENGINE = Kafka
SETTINGS 
    kafka_broker_list = 'kafka1:9092',
    kafka_topic_list = 'kafka-topic-2',
    kafka_group_name = 'test-group-2',
    kafka_format = 'JSONEachRow', 
    kafka_num_consumers = 1,
    kafka_skip_broken_messages = 10
;
```

```sql
CREATE TABLE kafka_test
(
    event_id UInt16,
    key String,
    value String,
    comment Nullable(String),
    topic String,
    partition UInt64
)
ENGINE = MergeTree
PRIMARY KEY (event_id)
ORDER BY event_id
;
```

```bash
docker exec -it clickhouse bash -lc \
'clickhouse-client --query "select * FROM system.kafka_consumers";'
```

```sql
CREATE MATERIALIZED VIEW kafka_queue_mv TO kafka_test
AS
SELECT
       event_id,
       key,
       value,
       comment,
       _topic AS topic,
       _partition AS partition
FROM kafka_queue
;
```

```bash
kafka-topics --bootstrap-server kafka1:9092 \
  --topic kafka-topic-2 \
  --describe
```

Send a test message
```bash
echo '{"event_id":1,"key":"hello","value":"world","comment":null}' | \
kafka-console-producer \
  --bootstrap-server kafka1:9092 \
  --topic kafka-topic-2
```

### Demo
![demo](./task_18.gif)


### Custom pipeline

-- custom producer/consumer

[producer.py](./producer.py)

[consumer.py](./consumer.py)

### Demo
![demo](./task_18_1.gif)
