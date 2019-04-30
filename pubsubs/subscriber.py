""" Abstract base class for the subscriber."""
import logging
import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta


class Subscriber(metaclass=InterfaceMeta):
    """ Abstract Subscriber."""

    BACKENDS = None

    def __init__(self, config, topics, serializer, **subscriber_config):
        self.config = config
        self.topics = topics
        #: Serializes the message received while listening
        self.serializer = serializer
        self.subscriber_config = subscriber_config

    def listen(self):
        """ Blocks until a message is received."""
        logging.info("Subscriber listening..")
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
        if backend not in cls._backends:
            raise KeyError(f"Missing '{backend}' implementation")
        return functools.partial(cls._backends[backend], backend=backend)

    @classmethod
    def __register_implementation__(cls):
        if not hasattr(cls, "_backends"):
            cls._backends = {}

        cls._backends[cls.__name__] = cls

        registry_keys = getattr(cls, "BACKENDS", []) or []
        if registry_keys:
            for key in registry_keys:
                if key in cls._backends and cls.__name__ != cls._backends[key].__name__:
                    raise NameError("Key already registered")
                else:
                    cls._backends[key] = cls
