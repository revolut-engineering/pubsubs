""" Abstract base class for the subscriber."""
import logging
from abc import abstractmethod

from interface_meta import InterfaceMeta

from pubsubs.exceptions import PubSubKeyError
from pubsubs.exceptions import PubSubNotFound


class Subscriber(metaclass=InterfaceMeta):
    """ Abstract Subscriber."""

    INTERFACE_EXPLICIT_OVERRIDES = True
    INTERFACE_RAISE_ON_VIOLATION = True
    BACKENDS = None

    def __init__(self, config, topics, serializer):
        self.config = config
        self.topics = topics
        #: Serializes the message received while listening
        self.serializer = serializer

    def listen(self):
        """ Blocks until a message is received."""
        logging.info(f"Subscriber listening to topics: {self.topics}")
        message = next(self)
        return self.serializer(message)

    def connect(self):
        self._connect()
        return self

    @abstractmethod
    def __next__(self):
        """ Return next message from the queue."""
        raise NotImplementedError

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @classmethod
    def for_backend(cls, backend):
        """ Retrieve concrete subscriber by name `backend`."""
        if backend not in cls._backends:
            raise PubSubNotFound(
                f"Missing subscriber implementation for '{backend}' backend."
            )
        return cls._backends[backend]

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
