""" Test base message queue consistency."""

from unittest.mock import Mock, patch

from pubsubs.dummy import DummyClient
from pubsubs.dummy import DummySubscriber
from pubsubs.registry import Registry


@patch.object(DummyClient, "_connect", Mock())
def test_connect_called_once():
    """ Test if '_connect' is called when retrieving new object
    from registry.
    """
    config = {"listeners": "localhost:8080"}
    registry = Registry()
    registry.new(name="test", backend="dummy", **config)

    dummy = registry["test"]
    dummy._connect.assert_called_once()


@patch.object(DummyClient, "_connect", Mock())
def test_connect_not_called():
    """ Test if '_connect' is only called once even after publish.
    """
    config = {"listeners": "localhost:8080"}
    registry = Registry()
    registry.new(name="test", backend="dummy", **config)

    dummy = registry["test"]
    dummy.publish(topic="mytopic", message="howl1")
    dummy.publish(topic="mytopic", message="howl2")
    dummy.publish(topic="mytopic", message="howl3")
    dummy._connect.assert_called_once()


@patch.object(DummyClient, "_connect", Mock())
@patch.object(DummySubscriber, "_connect", Mock())
def test_connect_subscriber():
    """ Test if '_connect' is called when instantiating subscriber
    """
    config = {"listeners": "localhost:8080"}
    registry = Registry()
    registry.new(name="test", backend="dummy", **config)

    dummy = registry["test"]
    subscriber = dummy.subscribe(["mytopic"])
    message = subscriber.listen()

    assert message == "Dummy Message"
    subscriber._connect.assert_called_once()
