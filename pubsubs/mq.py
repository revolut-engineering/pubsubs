import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta

from pubsubs.subscriber import Subscriber


class MessageQueue(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, name, registry, backend, listeners, **config):
        #: name registered under
        self._name = name
        #: implementation config
        self.config = config
        #: name of implementation
        self.backend = backend
        #: the registry associated with this implementation
        self.registry = registry
        #: servers to bind to
        self.listeners = listeners

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

    @classmethod
    def for_backend(cls, backend):
        if backend not in cls._backends:
            raise KeyError(f"Missing '{backend} implementation")
        return functools.partial(cls._backends[backend], backend=backend)

    @property
    def name(self):
        return self._name

    def subscribe(self, *topics):
        self._connect()
        topics = list(topics)

        # Create a new subscriber from the message queue implementation
        return Subscriber.for_backend(self.backend)(
            self._config, topics, self.serializer, **self._sub_config
        ).connect()

    def publish(self, topic, message):
        self._connect()
        self._publish(topic, message)
        return "Delivered"

    @abstractmethod
    def _publish(self, topic, message):
        raise NotImplementedError

    @abstractmethod
    def _connect(self):
        raise NotImplementedError
