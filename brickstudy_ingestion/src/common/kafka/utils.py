import json


class KafkaUtil:
    def __init__(self) -> None:
        self.kafka_servers = ["kafka1:19091"]

    def send_data_to_kafka(self, kafka_topic, data):
        from kafka import KafkaProducer
        producer = KafkaProducer(bootstrap_servers=self.kafka_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(kafka_topic, data)
        producer.flush()


if __name__ == "__main__":
    producer = KafkaUtil()
    producer.kafka_servers = ["localhost:9091"]
    producer.send_data_to_kafka("mock-randomuser", "hello")
