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

config = {
    "listeners": ['localhost:9092'],
    "publisher": {
        "poll": 1.0,
        "message.timeout.ms": 1500,
    }
}

registry = Registry()

kafka = registry.new("kafka1", backend="kafka", **config)

kafka.publish(topic="MyTopic", message="hey!")
```

### Subscriber

Configuring a Kafka subscriber and using a yaml.

```yaml
pubsubs:
    myKafka:
        backend: kafka
        listeners: ['localhost:9092']
        publisher:
            poll: 1.0
            message.timeout.ms: 1500
        subscriber:
            poll: 0.1
            group.id: 'myGroup'
            auto.offset.reset: 'earliest'
```

New Subscriber instance

```python
from pubsubs.registry import Registry

CONFIG = <see-above>

registry = Registry()

# This is alternative to using 'Registry.new'
registry.register_from_config(CONFIG)

kafka = registry["myKafka"]
subscriber = kafka.subscribe("MyTopic", "news-topic")

while True:
    message = subscriber.listen()
    print(message)
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
