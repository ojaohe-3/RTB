## Simulator
This module simulates sensor data and sends it to RabbitMQ.
To start the simulator 4 different inputs has to be given, 
these are how many people, vehicles, structures and activities.
Activities can be seen as a measure of how long the simulator 
will emulate data. An activity is simply a point for an actor
or vehicle to move towards. Just as the other modules the
simulator is also fully `asyncio` based. The simulator uses the
default library for logging.

All messages that the simulator sends to RMQ will be sent to 
the exchange 'sim_exchange'. Depending on if the message is about
actors, structures or activities a routing key will be given specifying
which of these three categories that is being sent. The routing key is
simply which queue the exchange should forward the message to.

## Starting the simulator
To start the simulator a sim.dat file has to exist containing
number of humans, vehicles, structures and activities.
This can be done by running our test.py.

```
python test.py
```

If the sim.dat file exist the simulator can be started by running:

```
python main.py
```

The default behaviour for the simulator is to send messages until
all activities has been done. 

## Configuration
The simulator will look for a file named `config.toml` in the root
directory. 
```
[rabbitmq]
username = "my_username"
password = "my_password"
host = "my_host"
exchange = "sim_exchange"

[MongoDB]
hoshost = "my_host"
port = "my_port"
```