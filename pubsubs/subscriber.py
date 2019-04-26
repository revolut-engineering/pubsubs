import functools
from abc import abstractmethod

from interface_meta import InterfaceMeta


class Subscriber(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, config, topics, serializer, **subscriber_config):
        self.config = config
        self.topics = topics
        #: Serializes the message received while listening
        self.serializer = serializer
        self.subscriber_config = subscriber_config

    def connect(self):
        self._connect()
        return self

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

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
