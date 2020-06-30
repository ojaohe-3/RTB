## ConsumerStructure
This module is responsible for collecting and storing data about the structures. This consumer is collecting messages from the queue called "structures" in RabbitMQ and that queue is binded to an exchange called "sim_exchange" in RMQ.

## Starting the Consumer
To start the consumer run:

```
python ConsumerStructure.py
```

Make sure you have a valid config file before running the application.

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
