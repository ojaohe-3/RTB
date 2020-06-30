## RabbitMQ

The central message broker used by h2alsv is RabbitMQ. This page gives you an
introduction on how to integrate your module with the RMQ configuration.

## Server configuration

The server uses the default AMQP port `5672` for connected clients.

Server settings can be configured from the RabbitMQ Web UI. The Web UI is accessible
from port `15672`.

Required login credentials and server IP address can be found in the h2alsv Google Sheet.

## Sending Sensor Data to the RMQ server

All sensor data is sent to the same exchange with the following details:

* Exchange name: `sim_exchange`
* Type: `DIRECT`
* Durable: `True`
 
Since the exchange is the type DIRECT, a routing key has to be specified. This key specifies which queue
the message should be sent to. If the exchange were of the type FANOUT any message to the exchange would be sent to
all the queues binded to that exchange.

To connect to RabbitMQ and declare the exchange from the `aio_pika` python library:

```python
import asyncio
import aio_pika


connection = await connect("amqp://user:pass@localhost/")
channel = await connection.channel()
sensor_exchange = await channel.declare_exchange('sim_exchange', aio_pika.ExchangeType.FANOUT, durable=True)
message_body = "Hello World".encode()
message = aio_pika.Message(body=message_body)
await sensor_exchange.publish(message, routing_key='')
```

Remember that all data sent to the `sim_exchange` exchange must follow the
```
[h2alsv protocol](general/h2alsv_protocol.md).
```
## Consuming Sensor Data

A consumer module is responsible to create and delete queues and binding them
to the `sim_exchange` exchange.

An an example implementation with the `aio_pika` library can be seen below.


```python
import asyncio
import aio_pika


connection = await connect("amqp://user:pass@localhost/")
channel = await connection.channel()
await channel.set_qos(prefetch_count=1)
sensor_exchange = await channel.declare_exchange('sim_exchange', aio_pika.ExchangeType.FANOUT, durable=True)
queue = await channel.declare_queue()
await queue.bind(sensor_exchange)

buffer = asyncio.Queue()

async with queue.iterator() as queue_iter:
    async for message in queue_iter:
        async with message.process():
            await buffer.put(message.body.decode())
```

