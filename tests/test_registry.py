""" Test the pubsub registry."""

import pytest

from pubsubs.base import MessageQueue
from pubsubs.base import Subscriber
from pubsubs.registry import Registry
from pubsubs.exceptions import PubSubKeyError


def test_registry_assign_same_name():
    """ Test assigning same name in registry raises."""
    config = {"listeners": "localhost:8080"}
    registry = Registry()

    registry.new(name="test", backend="dummy", **config)
    with pytest.raises(PubSubKeyError):
        registry.new(name="test", backend="dummy", **config)


def test_registry_get_instances():
    """ Test retrieving instances."""
    config = {"listeners": "localhost:8080"}
    registry = Registry()

    registry.new(name="test", backend="dummy", **config)
    dummy = registry["test"]
    subscriber = dummy.subscribe("test")
    assert isinstance(dummy, MessageQueue)
    assert isinstance(subscriber, Subscriber)


def test_registry_contains():
    """ Test checking registry for instance by name."""
    config = {"listeners": "localhost:8080"}
    registry = Registry()
    registry.new(name="test", backend="dummy", **config)

    assert "test" in registry
    assert "new-test" not in registry
