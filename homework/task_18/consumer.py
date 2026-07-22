import json
import sys

from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

BOOTSTRAP_SERVERS = "localhost:29092"
TOPIC = "kafka-topic-2"
client = Client(
    host="localhost",
    port=9000,
    user="baseline_user",
    password="baseline_pass",
)


def handler(message: ConsumerRecord) -> None:
    data = json.loads(message.value)
    client.execute(
        """
        INSERT INTO kafka_test (event_id, `key`, value, comment, topic, partition)
        VALUES
        """,
        [
            (
                data["event_id"],
                data["key"],
                data["value"],
                data.get("comment"),
                message.topic,
                message.partition,
            )
        ],
    )


def main() -> int:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="kafka-group-test",
    )

    try:
        for message in consumer:
            print(
                f"Received {message.topic}[{message.partition}]@{message.offset}: {message.value}",
                flush=True,
            )
            handler(message)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
