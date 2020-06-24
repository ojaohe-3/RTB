import pickle

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

sendData = ''
activites = []
structures = []
actors = []
map = Map()
conf = {}


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
        logger.info("Sending message to RMQ")
        await self._exchange.publish(
            aio_pika.Message(
                body=msg.encode()
            ),
            routing_key=routing_key)

    def get_sensor_data(self, actor):
        logger.info("Creating sensor data")
        cur_time = datetime.datetime.now().time()
        json_msg = {
            "time": str(cur_time),
            "type": actor.__name__,
            "payload": actor.toJson()
        }
        return json.dumps(json_msg)



def moveActorTowards(actor, pos,structures,activites):
    actor.updatePos(pos)
    hit, obj = checkForCollisions(actor,structures,activites)
    if (hit):
        # todo if this does return an delta vector, that is the required difference to displace the shapes, then translate to point.
        # not to mention all the errors in the universe
        displacement = checkCollisionDisplacment(obj, actor.bounds)
        actor.setPos(displacement)


def checkForCollisions(actor,structures,activites):
    mapbound = map.shape
    # inside of map
    if (not checkCollision(mapbound, actor.bounds)):
        #logger.info(f"{actor.name} is out of bounds! {str(actor.pos)}")
        return False, mapbound
    # all placed structures
    for structure in structures:
        shape1 = structure.shape
        if checkCollision(shape1, actor.bounds):
            print(f"{actor.name} collided with a structure at {str(actor.pos)}")
            return True, shape1
    # all placed activites
    for activity in activites:
        if activity.isActive():
            shape1 = activity.bounds
            if (checkCollision(shape1, actor.bounds)):
                logger.info(f"{actor.name} arrived at a activity {str(activity.pos)}, completeing it")
                activity.status = 'completed'
                # todo make event

                return True, shape1
    # other actors, if we care to
    # for a in actors:
    #     if(a != actor):
    #         if(checkCollision(a.bounds,actor.bounds)):
    #             return True, a.bounds
    return False, None

def checkCollision(shape1, shape2):
    s1 = shape1
    s2 = shape2

    for shape in range(0, 2):
        # reverse the entire process to project onto the normal of the inital projection vector
        if shape == 1:
            s1 = shape2
            s2 = shape1
        for i in range(0, len(s2)):
            point1 = s2[i]
            x1 = point1[0]
            y1 = point1[1]

            point2 = s2[(i + 1) % len(s2)]
            x2 = point2[0]
            y2 = point2[1]

            # A projected vector, normal between 2 points in the shape that collision will be projected against
            P = (-(y2 - y1), (x2 - x1))

            max1 = -9999999
            min1 = 9999999
            # discover the maximum length of any projected line of the shape on projection vector P
            for j in range(0, len(s2)):
                point = s2[j]
                x = point[0]
                y = point[1]
                Q = P[0] * x + P[1] * y
                max1 = max(max1, Q)
                min1 = min(min1, Q)

            # project against the other shape and take the maximum length of a line
            max2 = -9999999
            min2 = 9999999
            for k in range(0, len(s1)):
                point = s1[k]
                x = point[0]
                y = point[1]
                Q = P[0] * x + P[1] * y
                max2 = max(max2, Q)
                min2 = min(min2, Q)

            # if any of the shapes orthogonal projected vector where to not intersect with the other shapes projection, then there cannot be any collision

            if not (max2 >= min1 and max1 >= min2):
                return False
    return True


def checkCollisionDisplacment(shape1, shape2):
    s1 = shape1
    s2 = shape2
    dx = 0
    dy = 0
    for shape in range(0, 2):
        # reverse the entire process to project onto the normal of the inital projection vector
        if shape == 1:
            s1 = shape2
            s2 = shape1

        pos = findCentroid(s2)
        for p in s1:
            for i in range(0, len(s2)):
                qs = s2[i]
                qe = s2[(i + 1) % len(s2)]
                # i dunno man, line segment algoritm, or something
                h = (qe[0] - qs[0]) * (pos[1] - p[1]) - (qe[1] - qs[1]) * (pos[0] - p[0])
                t1 = ((qs[1] - qe[1]) * (pos[0] - qs[0]) + (qs[0] - qe[0]) * (pos[1] - qs[1])) / h
                t2 = ((pos[1] - p[1]) * (pos[0] - qs[0]) + (pos[1] - p[1]) * (pos[1] - qs[1])) / h

                # collision detected condition
                if t1 >= 0 and t1 < 1 and t2 >= 0 and t2 < 1:
                    # The second shape to our reference need to be subtracted to the final displacement
                    if shape == 0:
                        dx += (1 - t1) * (p[0] - pos[0])
                        dy += (1 - t1) * (p[1] - pos[1])
                    else:
                        dx -= (1 - t1) * (p[0] - pos[0])
                        dy -= (1 - t1) * (p[1] - pos[1])
    return [dx,dy]

# credit https://progr.interplanety.org/en/python-how-to-find-the-polygon-center-coordinates/
def findCentroid(vertexes):
    x = [vertex[0] for vertex in vertexes]
    y = [vertex[1] for vertex in vertexes]
    length = len(vertexes)
    x0 = sum(x) / length
    y0 = sum(y) / length
    return [x0, y0]


async def main(loop):
    config = toml.load('config.toml')
    with open("sim.dat", "rb") as f:
        data = pickle.load(f)
        actors = data["actors"]
        structures = data["structures"]
        activites = data["activites"]

    sim = Emulator(config, loop)
    await sim.connect()
    while True:
        for a in actors:
            a.activity = activites[0]  # temp
            moveActorTowards(a, a.activity.pos,structures,activites)

        await asyncio.sleep(0.04)
    await sim.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()

