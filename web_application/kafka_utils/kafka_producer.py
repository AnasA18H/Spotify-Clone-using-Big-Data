from kafka import KafkaProducer
import json


class CustomKafkaProducer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_message(self, topic, message):
        self.producer.send(topic, json.dumps(message).encode("utf-8"))
