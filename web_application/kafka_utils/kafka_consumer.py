from confluent_kafka import Consumer, KafkaError

# Configure Kafka consumer
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",  # Start reading from the beginning of the topic
}

# Create Kafka consumer
consumer = Consumer(conf)

# Subscribe to Kafka topic
topic = "song_clicks"
consumer.subscribe([topic])

try:
    while True:
        # Poll for new messages
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, consumer reached end of topic
                continue
            else:
                # Other error
                print(msg.error())
                break

        # Print message value
        print("Received message: {}".format(msg.value().decode("utf-8")))

except KeyboardInterrupt:
    # Stop consuming
    consumer.close()
