""" Registry controlling access to pubsubs."""
import yaml

from pubsubs.base import MessageQueue
from pubsubs.exceptions import PubSubKeyError


class Registry:
    def __init__(self):
        self._registry = {}

    def new(self, *, name, backend, **kwargs):
        """ Register new instantiated concrete instance."""
        return self.register(
            MessageQueue.for_backend(backend)(name, registry=self, **kwargs).connect(),
            name=name,
        )

    def register(self, message_queue, name):
        """ Assign concrete concrete instance to a name."""
        name = message_queue.name if not name else name

        if name in self._registry:
            raise PubSubKeyError(f"PubSub {name} exists.")

        self._registry[name] = message_queue
        return message_queue

    def __getitem__(self, name):
        return self._registry[name]

    def __contains__(self, name):
        return name in self._registry

    def register_from_config(self, config):
        """ Expects yaml in the form of text.
        Format compatible with 'omniduct'

        See:
        https://github.com/airbnb/omniduct/blob/master/example_wrapper/example_wrapper/services.yml
        """
        config = self._process_config(config)

        for mq_config in config:
            name = mq_config.pop("name")
            backend = mq_config.pop("backend")
            self.new(name=name, backend=backend, **mq_config)

        return self

    def _process_config(self, config):
        """ Load yaml as string into dict."""
        config = yaml.safe_load(config)

        pubsub_config = config.pop("pubsubs")
        for name, kwargs in pubsub_config.items():
            kwargs = kwargs.copy()
            kwargs["name"] = name
            yield kwargs
