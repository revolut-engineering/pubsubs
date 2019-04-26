<h1 align='center'>
    Pubsubs
</h1>

<h4 align='center'>
    Uniform pubsub interface for kafka
</h4>


## Installing

```
pip install pubsubs
```

## Usage

```python
from pubsubs.registry import Registry


CONFIG = """\
kafka:
    backend: kafka
    message.timeout.ms: 1500
    bootstrap.servers:
        - localhost:9092
"""

registry = Registry()
registry.register_from_config(CONFIG)

message_queue = registry["kafka"]

message_queue.publish(topic="NeW-Topic", message="hey!")

subscriber = message_queue.new_subscriber('topic1', 'topic2')
```
