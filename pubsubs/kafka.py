""" Concrete kafka implementation."""
import logging

from interface_meta import override

from pubsubs.base import MessageQueue, Subscriber


class KafkaClient(MessageQueue):
    """ Concrete client implementation of Kafka."""

    BACKENDS = ["kafka"]

    @override
    def _connect(self):
        from confluent_kafka import Producer

        self._prepare()
        self._producer = Producer(self._config)

    def _prepare(self):
        """ Prepare kafka configuration."""
        # Configuration for publisher
        self._config = self.config.pop("publisher")
        self._poll = self._config.pop("poll")

        servers = ",".join(self.listeners)
        self._config.update({"bootstrap.servers": servers})

        # Configuration for subscriber
        self._subscriber_config = self.config.pop("subscriber")

    @override
    def _publish(self, topic, message):
        """ Kafka implementation of publish."""

        def delivery_report(err, msg):
            if err is not None:
                logging.exception("Message failed: {}".format(err))
            else:
                logging.debug(
                    "Message delivered, topic: {}, partition: {}, offset".format(
                        msg.topic(), msg.partition(), msg.offset()
                    )
                )

        self._producer.poll(self._poll)
        self._producer.produce(topic, message, callback=delivery_report)
        self._producer.flush()

    @override
    def _serializer(self, message):
        return message.value().decode("utf-8")


class KafkaSubscriber(Subscriber):
    """ Concrete Kafka subscriber."""

    BACKENDS = ["kafka"]

    @override
    def _connect(self):
        from confluent_kafka import Consumer

        self._poll = self.config.pop("poll")
        self._consumer = Consumer(self.config)
        self._consumer.subscribe(self.topics)

    @override
    def __next__(self):
        while True:
            msg = self._consumer.poll(self._poll)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error {msg.error()}")
            if msg:
                return msg
