import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta


class MessageQueue(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, name, registry, backend, listeners, **kwargs):
        self._name = name
        self.backend = backend
        self.registry = registry
        self.listeners = listeners

        self.config = kwargs
        self._subscriber = self._assign_subscriber()

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
        return self._subscriber(self._config, topics, **self._sub_config)

    def _assign_subscriber(self):
        return Subscriber.for_backend(self.backend)

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


class Subscriber(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, serializer, **kwargs):
        self.serializer = serializer

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
            raise KeyError(f"Missing '{backend}' implementation")
        return functools.partial(cls._backends[backend], backend=backend)

    def listen(self):
        """ Blocks until a message is received."""
        message = next(self)
        return self.serializer(message)

    @abstractmethod
    def __next__(self):
        raise NotImplementedError
