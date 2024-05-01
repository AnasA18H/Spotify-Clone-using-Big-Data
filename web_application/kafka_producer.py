from kafka import KafkaProducer
import json


def send_message(topic, message):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    producer.send(topic, value=message)
    producer.flush()
