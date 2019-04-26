<h1 align='center'>
    PubSubs
</h1>

<h4 align='center'>
    Uniform pubsub interfaces
</h4>


## Installing

```
pip install pubsubs
```

## Usage

### Publisher

Configuration

```yaml
kafka:
    backend: kafka
    listeners::
        - localhost:9092
    poll: 0
    message.timeout.ms: 1500
```

New publisher

```python
from pubsubs.registry import Registry

CONFIG = <see-above>

registry = Registry()
registry.register_from_config(CONFIG)

message_queue = registry["kafka"]

message_queue.publish(topic="MyTopic", message="hey!")
```

### Subscriber

Configuration

```yaml
kafka:
    backend: kafka
    listeners: ['localhost:9092']
    poll: 0.1
    group.id: 'myGroup'
    auto.offset.reset: 'earliest'
```

New Subscriber

```python
from pubsubs.registry import Registry

CONFIG = <see-above>

registry = Registry()
registry.register_from_config(CONFIG)

message_queue = registry["kafka"]
subscriber = message_queue.subscribe("MyTopic", "news-topic")

while True:
    next_message = subscriber.listen()
    print(next_message)
```
