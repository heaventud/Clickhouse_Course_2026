import json
import sys

from kafka import KafkaProducer


BOOTSTRAP_SERVERS="localhost:29092"
TOPIC = "kafka-topic-2"

def main() -> int:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    event = {
        "event_id": 6,
        "key": "key_6",
        "value": "value_6",
        "comment": None,
    }

    producer.send(TOPIC, value=event)
    producer.flush()
    producer.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
