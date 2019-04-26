from interface_meta import override

from pubsubs.mq import MessageQueue


class KafkaSubscriber:
    pass


class KafkaClient(MessageQueue):

    BACKENDS = ["kafka"]

    @override
    def _connect(self):
        from confluent_kafka import Producer

        _SETTINGS = {
            "bootstrap.servers": "localhost:9092",
            "message.timeout.ms": "1500",
        }
        self._producer = Producer(_SETTINGS)

    @override
    def _new_subscriber(self, *topics):
        return KafkaSubscriber()

    @override
    def _publish(self, topic, message):
        def delivery_report(err, msg):
            if err is not None:
                print("Message failed: {}".format(err))
            else:
                print("Message delivered")

        self._producer.poll(0)
        self._producer.produce(topic, message, callback=delivery_report)
        self._producer.flush()
