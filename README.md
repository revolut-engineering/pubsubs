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
from pubsubs.pubsubs import Registry

CONFIG = """\
kafka:
    backend: kafka
    message.timeout.ms: 1500
    bootstrap.servers:
        - localhost:9092
"""
register = Registry()
reg = register.register_from_config(CONFIG)

ps = reg["kafka"]
ps.publish(topic="NeW-Topic", message="hey!")
```
