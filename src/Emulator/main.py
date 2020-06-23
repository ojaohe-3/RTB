import asyncio
import aio_pika
import datetime
import json
import logging
import sys
import toml
# from activity import Activity
# from actor import Actor
# from structure import Structure
# from timewrapper import TimeWrapper
# from map import Map
from functools import wraps
config = toml.load('config.toml')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename=config['log']['filename'])

out_handler = logging.StreamHandler(sys.stdout)
out_handler.setLevel(logging.DEBUG)
logger.addHandler(out_handler)

sendData = ''
workers = []
trucks = []
activites = []
structures = []
#map = Map()


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
            "event_type": actor.type,
            "event_activity": actor.activity,
            "event_position": actor.pos,
            "event_velocity": actor.vel,
        }
        return json.dumps(json_msg)



async def main(loop):
    # print("generating senario from config file")
    # conf = {}
    # activites = conf["activites"]
    # workers = conf["workers"]
    # trucks = conf["trucks"]
    # strutures = conf["structures"]
    config = toml.load('config.toml')
    sim = Emulator(config,loop)
    await sim.connect()
    await sim.disconnect()
if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()

def connectionSetup():
    return


def sendData():
    msg = ''
    if 'not setup' == 'setup':
        connectionSetup()
    return 'completed ' + msg


def collisionDetection(func):
    @wraps(func)
    def wrapper(boundBox, vel):
        bounds = []
        for point in boundBox:
            bounds.append(point)
        # create local copy
        mapbound = map.shape
        # test for map shape

        # all placed structures
        for structure in structures:
            # extract shape of each indivudual structure
            shape1 = structure.pointMap
            # test for collision of object
            if checkCollision(shape1, bounds):
                # this system does only allow Convex shapes to exist for simplisity, thus no wall will be greater than 90º vel simply can bounce
                print("collision detected")
                # collision
        # test for activity collision
        boundBox = bounds
        return func(boundBox, vel)

    return wrapper


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
                max1 = max(max, Q)
                min1 = min(min, Q)

            # project against the other shape and take the maximum length of a line
            max2 = -9999999
            min2 = 9999999
            for k in range(0, len(s1)):
                point = s1[k]
                x = point[0]
                y = point[1]
                Q = P[0] * x + P[1] * y
                max2 = max(max, Q)
                min2 = min(min, Q)

            # does the maximum length of the projected bounds vs projected shape1 overlap? if so there is collision

            if not (max2 >= min1 and max1 >= min2):
                return 0
    return 1


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

    return (dx, dy)


# credit https://progr.interplanety.org/en/python-how-to-find-the-polygon-center-coordinates/
def findCentroid(vertexes):
    x = [vertex[0] for vertex in vertexes]
    y = [vertex[1] for vertex in vertexes]
    length = len(vertexes)
    x0 = sum(x) / length
    y0 = sum(y) / length
    return (x0, y0)
