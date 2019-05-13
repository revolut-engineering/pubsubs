""" Abstract base class, controls the interface for pub/sub implementations."""
import logging
import functools
from abc import abstractmethod

from interface_meta import quirk_docs
from interface_meta import InterfaceMeta

from pubsubs.subscriber import Subscriber
from pubsubs.exceptions import PubSubKeyError
from pubsubs.exceptions import PubSubNotFound


class MessageQueue(metaclass=InterfaceMeta):
    """ Abstract Base Class."""

    INTERFACE_EXPLICIT_OVERRIDES = True
    INTERFACE_RAISE_ON_VIOLATION = True
    BACKENDS = None

    def __init__(self, name, registry, listeners, **config):
        self.name = name
        self.registry = registry
        self.listeners = listeners
        self.config = config

    def subscribe(self, *topics):
        """ Return a subscriber instance associated to the concrete
        implementation.
        """
        topics = list(topics)

        # Initialise new subscriber from the name of concrete class
        return Subscriber.for_backend(self.backend)(
            self.subscriber_config, topics, self._serializer
        ).connect()

    def connect(self):
        """ Connect to client implementation."""
        self._connect()
        return self

    @quirk_docs("_publish")
    def publish(self, topic, message):
        """ Publish `message` to the `topic`."""
        self._publish(topic, message)
        logging.info(f"'{message}' published to '{topic}'")

    @property
    def subscriber_config(self):
        """ Configuration of associated subscriber."""
        return self._subscriber_config

    @abstractmethod
    def _serializer(self, message):
        """ Format message received by the implementation."""
        raise NotImplementedError

    @abstractmethod
    def _publish(self, topic, message):
        raise NotImplementedError

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @classmethod
    def for_backend(cls, backend):
        """ Retrieve concrete implementation by name `backend`."""
        if backend not in cls._backends:
            raise PubSubNotFound(
                f"Missing publisher implementation for '{backend}' backend."
            )
        return functools.partial(cls._backends[backend])

    @classmethod
    def __register_implementation__(cls):
        """ Register concrete child classes inheriting this base class.

        Method called by metaclass 'InterfaceMeta'.
        """
        if not hasattr(cls, "_backends"):
            cls._backends = {}

        cls._backends[cls.__name__] = cls

        registry_keys = getattr(cls, "BACKENDS", []) or []
        if registry_keys:
            for key in registry_keys:
                if key in cls._backends and cls.__name__ != cls._backends[key].__name__:
                    raise PubSubKeyError("Implementation already registered")
                else:
                    cls._backends[key] = cls
