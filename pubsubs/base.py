""" Abstract base class, controls the interface for pub/sub implementations."""
import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta

from pubsubs.subscriber import Subscriber


class MessageQueue(metaclass=InterfaceMeta):
    """ Abstract Base Class."""

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
            self._config, topics, self.serializer, **self._sub_config
        ).connect()

    def publish(self, topic, message):
        """ Publish `message` to the `topic`."""
        self._connect()
        self._publish(topic, message)
        return "Delivered"

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
        """ Register concrete child classes inheriting this base class."""
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
