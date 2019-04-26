import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta


class MessageQueue(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, name, registry, backend, **kwargs):
        self._name = name
        self.backend = backend
        self.registry = registry

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
        return self._new_subscriber(topics)

    def publish(self, topic, message):
        self._connect()
        self._publish(topic, message)
        return "Delivered"

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abstractmethod
    def _publish(self, topic, message):
        raise NotImplementedError

    @abstractmethod
    def _new_subscriber(self, *topics):
        raise NotImplementedError
