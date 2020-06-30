## ConsumerEvent
This module is responsible to collect and store data about all the events/activities. It collects messages from the queue "events" in RabbitMQ which is binded to the exchange "sim_exchange" in RMQ.

To start the consumer run:

```
python ConsumerEvent.py
```

Make sure you have a valid config file before starting. 

## Configuration
The module will look for a file named
'config.toml' in the root directory. 
RabbitMQ and MongoDB are important settings
that has to be correctly configured in order for the application to run.

The config file is structured as the example below.´

```
[rabbitmq]
username = "my_username"
password =` "my_password"
host = "my_host"
sensor_exchange = "sensor_data"
queue = "structure_queue"

[MongoDB]
hoshost = "my_host"
port = "my_port"
```