from interface_meta import override

from pubsubs.mq import MessageQueue, Subscriber


class KafkaClient(MessageQueue):

    BACKENDS = ["kafka"]

    @override
    def _connect(self):
        from confluent_kafka import Producer

        self._prepare()
        self._producer = Producer(self._config)

    def _prepare(self):
        # Configuration for subscriber
        poll = self.config.pop("poll")
        self._sub_config = {"poll": poll}

        # Configuration for publisher
        servers = ",".join(self.listeners)
        self._config = {"bootstrap.servers": servers}
        self._config.update(self.config)

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

    def serializer(self, message):
        return message.value().decode("utf-8")


class KafkaSubscriber(Subscriber):

    BACKENDS = ["kafka"]

    def _connect(self):
        from confluent_kafka import Consumer

        self._poll = self.subscriber_config.pop("poll")
        self._consumer = Consumer(self.config)
        self._consumer.subscribe(self.topics)

    def __next__(self):
        while True:
            msg = self._consumer.poll(self._poll)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error {msg.error()}")
            if msg:
                return msg
