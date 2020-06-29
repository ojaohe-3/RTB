import pickle
import random
from src.Emulator.collision import separating_axis_theorem
from src.Emulator.activity import Activity
from src.Emulator.actor import Actor
from src.Emulator.structure import Structure
from src.Emulator.timewrapper import TimeWrapper
from src.Emulator.map import Map
import asyncio
import aio_pika
import datetime
import json
import logging
import sys
import toml

from functools import wraps

config = toml.load('config.toml')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=config['log']['filename'])

out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.DEBUG)
logger.addHandler(out_handler)


class Emulator:
    def __init__(self, config, loop):
        self.config = config
        self.loop = loop
        self._connection = None
        self._channel = None
        self._exchange = None
        self._simTasks = []
        self._running = False

    async def _create_connection(self):
        logger.info("Creating connection to RMQ")
        return await aio_pika.connect_robust("amqp://{}:{}@{}/".format(
            self.config['rabbitmq']['username'],
            self.config['rabbitmq']['password'],
            self.config['rabbitmq']['host'],
        ), loop=self.loop)

    async def connect(self):
        logger.info("Connecting to RMQ")
        # creates the connection to RabbitMQ
        self._connection = await self._create_connection()
        # Creates the channel on RabbitMQ
        self._channel = await self._connection.channel()
        # Declares the exchange on the channel on RabbitMQ
        self._exchange = await self._channel.declare_exchange('sensor_exchange', aio_pika.ExchangeType.FANOUT,
                                                              durable=True)

    async def disconnect(self):
        logger.info("Disconnecting from RMQ")
        await self._connection.close()
        self._channel = None
        self._exchange = None
        self._running = False

    async def send_message(self, msg, routing_key):
        #logger.info("Sending message to RMQ")
        await self._exchange.publish(
            aio_pika.Message(
                body=msg.encode()
            ),
            routing_key=routing_key)

    def get_sensor_data(self, object):
        #logger.info("Creating sensor data")
        cur_time = datetime.datetime.now().time()
        json_msg = {
            "time": str(cur_time),
            "type": type(object).__name__,
            "payload": object.toJson()

        }
        return json.dumps(json_msg)


def moveActorTowards(actor, pos, structures, activites):
    actor.updatePos(pos)
    if(checkForCollisions(actor, structures, activites)):
        print(f"collision deteced, {actor.name} have collided at {str(actor.pos)}")
        actor.updatePos([-1*x+random.random()*2 for x in pos])



def checkForCollisions(actor, structures, activites):
    mapbound = Map().shape
    # inside of map
    if (not separating_axis_theorem(mapbound, actor.shape)):
        print(f"\033[93m{actor.name} is out of bounds! {str(actor.pos)} \033[0m")
        return True

    if (separating_axis_theorem(actor.activity.shape, actor.shape)):
        # logger.info(f"{actor.name} arrived at a activity {str(activity.pos)}, completeing it")
        print(f"\n\n\033[92m{actor.name} arrived at a activity {str(actor.activity.pos)}, completeing it \033[0m\n\n")
        actor.activity.status = 'completed'
        try:
            activites.pop(activites.index(actor.activity))

        except:
            actor.activity = None
        finally:
            if(len(activites)>1):
                actor.activity = activites[random.randrange(len(activites)-1)]
            else:
                exit(-1)
        print(f"\n\n\033[93m New Task Assigned! {len(activites)} tasks remains.\033[0m\n\n")

    for structure in structures:
        if (separating_axis_theorem(structure.shape,actor.shape)):
            return True
    return False


async def actorsPos(actors):
    for a in actors:
        print(f"\033[33m{a.name} is at pos {str(a.pos)} moving towards {str(a.activity.pos)}\033[0m")
    await asyncio.sleep(5)
    return await actorsPos(actors)


async def main(loop, actors, structures, activites):
    config = toml.load('config.toml')
    sim = Emulator(config, loop)
    await sim.connect()

    while True:
        for a in actors:
            moveActorTowards(a, a.activity.pos, structures, activites)
            msg = sim.get_sensor_data(a)
            await sim.send_message(msg, 'sensor_exchange')

        await asyncio.sleep(0.04)

        if len(activites) < 1:
            break
    await sim.disconnect()


def init():
    with open("sim.dat", "rb") as f:
        data = pickle.load(f)
        actors = data["actors"]
        structures = data["structures"]
        activites = data["activites"]
    for a in actors:
        a.activity = activites[random.randrange(len(activites) - 1)]

    return actors, structures, activites

async def multiTask(actors, structures, activites,loop):
    await asyncio.gather(actorsPos(actors),main(loop,actors, structures, activites))


if __name__ == "__main__":
    a, b, c = init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(multiTask(a,b,c,loop))
    loop.close()
