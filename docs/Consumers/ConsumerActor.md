## ConsumerActor
This module is responsible to collect data 
about all the actors in the simulation and 
storing it in a MongoDB. This consumer is 
collecting messages from the queue "Actors" 
in RabbitMQ and the queue is binded to an 
exchange called "sim_exchange". 

To start the consumer run:
```
python ConsumerActor.py
```

Make sure you have a valid config file before running the application.

## Configuration
The module will look for a file named
'config.toml' in the root directory. 
RabbitMQ and MongoDB are important settings
that has to be correctly configured in order for the application to run.

The config file is structured as the example below.

```
[rabbitmq]
username = "my_username"
password = "my_password"
host = "my_host"
sensor_exchange = "my_exchange"
queue = "actor_queue" 

[MongoDB]
hoshost = "my_host"
port = "my_port"
```

## Current Limitations 
??