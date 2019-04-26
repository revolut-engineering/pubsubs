import yaml

from pubsubs.mq import MessageQueue


class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, message_queue, name):
        name = message_queue.name if not name else name

        if name in self._registry:
            raise ValueError(f"PubSub {name} exists.")

        self._registry[name] = message_queue
        return message_queue

    def __getitem__(self, name):
        return self._registry[name]

    def __contains__(self, name):
        return name in self._registry

    def new(self, name, backend, **kwargs):
        return self.register(
            MessageQueue.for_backend(backend)(name, registry=self, **kwargs), name=name
        )

    def register_from_config(self, config):
        """ Expects yaml in the form of text."""
        config = self._process_config(config)

        for mq_config in config:
            name = mq_config.pop("name")
            backend = mq_config.pop("backend")
            self.new(name, backend, **mq_config)

        return self

    def _process_config(self, config):
        """ Load yaml as string into dict."""
        config = yaml.safe_load(config)
        for name, kwargs in config.items():
            kwargs = kwargs.copy()
            kwargs["name"] = name
            yield kwargs
