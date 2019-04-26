import functools
from abc import abstractmethod

import yaml
from interface_meta import InterfaceMeta


class PubSub(metaclass=InterfaceMeta):

    BACKENDS = None

    def __init__(self, name, registery, backend, **kwargs):
        self.backend = backend
        self._name = name

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

    @abstractmethod
    def _connect(self):
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    def subscribe(self, *topics):
        return self._new_subscriber(topics)

    def publish(self, topic, message):
        self._connect()
        self._publish(topic, message)
        return "Delivered"


class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, pubsub, name):
        name = pubsub.name if not name else name

        if name in self._registry:
            raise ValueError(f"PubSub {name} exists.")

        self._registry[name] = pubsub
        return pubsub

    def __getitem__(self, name):
        return self._registry[name]

    def __contains__(self, name):
        return name in self._registry

    def new(self, name, backend, **kwargs):
        return self.register(
            PubSub.for_backend(backend)(name, registery=self, **kwargs), name=name
        )

    def register_from_config(self, config):
        """ Expects yaml in the form of text."""
        config = self._process_config(config)

        for pubsub_config in config:
            name = pubsub_config.pop("name")
            backend = pubsub_config.pop("backend")
            self.new(name, backend, **pubsub_config)

        return self

    def _process_config(self, config):
        config = yaml.safe_load(config)
        for name, kwargs in config.items():
            kwargs = kwargs.copy()
            kwargs["name"] = name
            yield kwargs
