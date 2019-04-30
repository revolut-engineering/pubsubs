""" Abstract base class, controls the interface for pub/sub implementations."""
import logging
import functools
from abc import abstractmethod

from interface_meta import quick_docs
from interface_meta import InterfaceMeta

from pubsubs.subscriber import Subscriber


class MessageQueue(metaclass=InterfaceMeta):
    """ Abstract Base Class."""

    INTERFACE_EXPLICIT_OVERRIDES = True
    INTERFACE_RAISE_ON_VIOLATION = True
    BACKENDS = None

    def __init__(self, name, registry, backend, listeners, **config):
        self.name = name
        self.registry = registry
        #: The name of the implementation
        self.backend = backend
        self.listeners = listeners
        self.config = config

    def subscribe(self, *topics):
        """ Return a subscriber instance associated to the concrete
        implementation.
        """
        self._connect()
        topics = list(topics)

        # Initialise new subscriber from the name of concrete class
        return Subscriber.for_backend(self.backend)(
            self.subscriber_config, topics, self._serializer, **self.subscriber_config
        ).connect()

    @quick_docs("_publish")
    def publish(self, topic, message):
        """ Publish `message` to the `topic`."""
        self._connect()
        self._publish(topic, message)
        logging.info(f"'{message}' published to '{topic}'")
        return "Delivered"

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
            raise KeyError(f"Missing '{backend} implementation")
        return functools.partial(cls._backends[backend], backend=backend)

    @classmethod
    def __register_implementation__(cls):
        """ Register concrete child classes inheriting this base class.

        Method called by metaclass.
        """
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
