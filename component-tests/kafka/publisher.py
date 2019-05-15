""" Executed against a kafka instance in CI."""
import time

from pubsubs.registry import Registry

# Two minutes from now
TIMEOUT = time.time() + 60 * 2
CONFIG = """\
pubsubs:
    myKafka:
        backend: kafka
        listeners: ['kafka:9092']
        publisher:
            poll: 1.0
            message.timeout.ms: 3000
        subscriber:
            poll: 0.8
            group.id: mygroup
            auto.offset.reset: earliest
"""

registry = Registry()
registry.register_from_config(CONFIG)

kafka = registry["myKafka"]
kafka.publish(topic="mytopic", message="howl")


subscriber = kafka.subscribe("mytopic")

message = None
while not message:
    message = subscriber.listen()
    if time.time() > TIMEOUT:
        break

assert message == "howl"
