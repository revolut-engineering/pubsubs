<h1 align='center'>
    PubSubs
</h1>

<h4 align='center'>
    Uniform interfaces for Publishing and Subscribing
</h4>

---

This library allows you to decouple the publish/subscribe implementation
from your service.

## Installing

```
pip install pubsubs[<implementation-name>]
```

## Usage

### Publisher

New Kafka publisher instance

```python
from pubsubs.registry import Registry

CONFIG = """\
pubsubs:
    myKafka:
        backend: kafka
        listeners: ['localhost:9092']
        publisher:
            poll: 1.0
            message.timeout.ms: 1500
"""

registry = Registry()
registry.register_from_config(CONFIG)

kafka = registry["myKafka"]
kafka.publish(topic="mytopic", message="howl")
```

### Subscriber

Configuring a Kafka subscriber.

```python
from pubsubs.registry import Registry

config = {
    "listeners": ["localhost:9092"],
    "subscriber": {
        "poll": 0.1,
        "group.id": "mygroup",
        "auto.offset.reset": "earliest"
    },
}

registry = Registry()
kafka = registry.new(name="myKafka", backend="kafka", **config)

subscriber = kafka.subscribe("mytopic")
while True:
    message = subscriber.listen()
    print(message)
```

### Testing

```
make test
```

### Configuration

The subsection `pubsubs` in the yaml allows the config to be used along side
[omniduct](https://github.com/airbnb/omniduct/blob/master/example_wrapper/example_wrapper/services.yml)

| Name | Description | Example |
| ---- | ----------- | ------- |
| `backend` | Name of pub sub implementation | `backend: kafka` |
| `listeners` | List of serving addresses | `listeners: ['localhost:9092']` |
| `publisher` | Settings for the publisher | `publisher: {timeout: 1.0}` |
| `subscriber` | Settings for a subscriber | `subscriber: {timeout: 1.0}` |

#### Example config

The following is an example of setting up a config for kafka.

```yaml
pubsubs:
    kafka:
        backend: kafka
        listeners: ['localhost:9092']
        publisher:
            poll: 1.0
            message.timeout.ms: 1500
        subscriber:
            poll: 0.1
            group.id: 'myGroup'
            auto.offset.reset: 'earliest'

    kafkaPub:
        backend: kafka
        listeners: ['localhost:9092']
        publisher:
            poll: 1.0
            message.timeout.ms: 1500

    kafkaSub:
        backend: kafka
        listeners: ['localhost:9093']
        subscriber:
            poll: 0.1
            group.id: 'myGroup'
            auto.offset.reset: 'earliest'
```
