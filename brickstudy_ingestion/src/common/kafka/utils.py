import json


class Kafka:
    def __init__(self) -> None:
        self.kafka_servers = ["kafka1:19091"]

    def send_data_to_kafka(self, kafka_topic, data):
        from kafka import KafkaProducer
        producer = KafkaProducer(bootstrap_servers=self.kafka_servers,
                                 value_serializer=self.json_serializer)
        producer.send(kafka_topic, data)
        producer.flush()

    def get_data_from_kafka(self, kafka_topic):
        from kafka import KafkaConsumer
        consumer = KafkaConsumer(kafka_topic,
                                 bootstrap_servers=self.kafka_servers,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='my-group',  # 컨슈머 그룹 ID
                                 value_deserializer=self.json_deserializer)
        return consumer

    @staticmethod
    def json_serializer(data):
        return json.dumps(data).encode('utf-8')

    @staticmethod
    def json_deserializer(data):
        return json.loads(data.decode("utf-8"))


if __name__ == "__main__":
    message = {"key1": "value1"}
    topic = "test"

    produer = Kafka()
    produer.kafka_servers = ["localhost:9091"]
    produer.send_data_to_kafka(topic, message)

    consumer = Kafka()
    consumer.kafka_servers = ["localhost:9091"]
    result = consumer.get_data_from_kafka(topic)
    for msg in result:
        print(msg)
