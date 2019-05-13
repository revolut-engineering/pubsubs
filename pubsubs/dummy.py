""" Dummy implementation of message queue.

Intending for tests.
"""

from interface_meta import override

from pubsubs.base import Subscriber
from pubsubs.base import MessageQueue


class DummyClient(MessageQueue):
    """ Dummy client implementation."""

    BACKENDS = ["dummy"]
    backend = "dummy"

    @override
    def _connect(self):
        self._subscriber_config = {"dummy": "subscriber"}

    @override
    def _publish(self, topic, message):
        pass

    @override
    def _serializer(self, message):
        return message


class DummySubscriber(Subscriber):
    """ Dummy subscriber implementation."""

    BACKENDS = ["dummy"]
    backend = "dummy"

    @override
    def _connect(self):
        pass

    @override
    def __next__(self):
        return "Dummy Message"
