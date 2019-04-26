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

```
import pubsubs

pubsub = pubsubs.new('kafka')
pubsub = pubsubs.import_from_config(config)
pubsub = pubsubs.import_from_yaml('name: kafka')

subscriber = pubsub.subscribe('topicA', 'topicB') -> Variadic Args

pubsub.publish(topic='topic', message='message')

message = next(subscriber)
assert message == 'message'
```
