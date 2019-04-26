from pubsubs.pubsubs import PubSub


class KafkaSubscriber:
    pass


class KafkaClient(PubSub):

    BACKENDS = ["kafka"]

    def _connect(self):
        from confluent_kafka import Producer

        _SETTINGS = {
            "bootstrap.servers": "localhost:9092",
            "message.timeout.ms": "1500",
        }
        self._producer = Producer(_SETTINGS)

    def _new_subscriber(self):
        return KafkaSubscriber()

    def _publish(self, topic, message):
        def delivery_report(err, msg):
            if err is not None:
                print("Message failed: {}".format(err))
            else:
                print("Message delivered")

        self._producer.poll(0)
        self._producer.produce(topic, message, callback=delivery_report)
        self._producer.flush()
