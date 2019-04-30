<h1 align='center'>
    PubSubs
</h1>

<h4 align='center'>
    Uniform interfaces for Publishing and Subscribing
</h4>

This library allows you to decouple the publish/subscribe implementation
from your service.

## Installing

```
pip install pubsubs
```

## Usage

### Publisher

Configuring a Kafka publisher

```yaml
kafka:
    backend: kafka
    listeners::
        - localhost:9092
    poll: 0
    message.timeout.ms: 1500
```

New Kafka publisher instance

```python
from pubsubs.registry import Registry

CONFIG = <see-above>

registry = Registry()
registry.register_from_config(CONFIG)

kafka = registry["kafka"]
kafka.publish(topic="MyTopic", message="hey!")
```

### Subscriber

Configuring a Kafka subscriber

```yaml
kafka:
    backend: kafka
    listeners: ['localhost:9092']
    poll: 0.1
    group.id: 'myGroup'
    auto.offset.reset: 'earliest'
```

New Subscriber instance

```python
from pubsubs.registry import Registry

CONFIG = <see-above>

registry = Registry()
registry.register_from_config(CONFIG)

kafka = registry["kafka"]
subscriber = kafka.subscribe("MyTopic", "news-topic")

while True:
    message = subscriber.listen()
    print(message)
```
