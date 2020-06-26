import asyncio
import aio_pika
import toml
import logging
import sys
import json
import pymongo
from pymongo import MongoClient

config = toml.load('config.toml')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=config['log']['filename'])

out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.DEBUG)
logger.addHandler(out_handler)

class Consumer():
    def __init__(self, config):
        self.config = config
        #self.loop = loop

        self._connection = None
        self._channel = None
        self._exchange = None
    async def _create_connection(self):
        #logger.info("Creating connection")
        return await aio_pika.connect_robust(
                "amqp://{}:{}@{}".format(
                    self.config['rabbitmq']['username'],
                    self.config['rabbitmq']['password'],
                    self.config['rabbitmq']['host'],
                )
        )
    async def connect(self):
        #logger.info("Connecting to RMQ")
        self._connection = await self._create_connection()
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
        self.config['rabbitmq']['sensor_exchange'], aio_pika.ExchangeType.FANOUT, durable=True
        )

        self._queue = await self._channel.declare_queue(exclusive=True)
        await self._queue.bind(self._exchange)
        logger.info("connected to RMQ")

    async def disconnect(self):
        logger.info("Closing connection to RMQ")
        await self._connection.close()
        self._connection = None
        self._channel = None
        self._exchange = None
        self._running = False

    async def consume(self, mongo):
        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    #logger.info("Consuming")
                    #logger.info(message.body)
                    msg = json.loads(message.body)
                    logger.info("POSITION")
                    logger.info(msg['payload']['position'])

                    actor = msg['payload']['name']
                    actorPosition = msg['payload']['position']
                    actorShape = msg['payload']['shape']

                    mongo.update(
                        { "Name" : actor},
                            {
                                "$set": {"position": actorPosition,
                                         "shape": actorShape}
                            },
                            upsert=True

                        )
                    logger.info('mongoupdated')

                    #await self.buffer.put(message.body.decode())
                    #if queue.name in message.body.decode():
                     #   break
async def main():
    config = toml.load("config.toml")
    consumer = Consumer(config)
    client = MongoClient("mongodb://{}:{}/".format(config["MongoDB"]["host"],config["MongoDB"]["port"]))
    rtbDB = client['rtb']
    actorCol = rtbDB['Actors']

    await consumer.connect()
    await consumer.consume(actorCol)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()