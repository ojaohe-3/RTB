from src.Consumer import Consumer
import toml
import asyncio
from pymongo import MongoClient
from quart import Quart, jsonify
from quart import render_template

app = Quart(__name__)


class DB(object):
    @staticmethod
    def get_connection():
        config = toml.load("config.toml")
        return MongoClient(f"mongodb://{config['MongoDB']['host']}:{config['MongoDB']['port']}")


@app.route('/')
async def index():
    return await render_template("konva.html", info={"title": "Construction Test Site"})


@app.route('/data')
async def sendRequesterData():
    print("got a data request")
    # todo authentication
    # todo get data from socket if available
    # todo generate json and send to requester
    db = DB.get_connection()
    collection = db["rtb"].get_collection("Actors").find({})
    msg = {}
    for obj in iter(collection):
        temp = {}
        for value in obj:
            if '_id' not in value and 'Name' not in value:
                temp[value] = obj[value]
        msg[str(obj['Name'])] = temp
    return str(msg)


async def getData(conf, loop):
    return ''


loop = asyncio.get_event_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run()
    config = toml.load("config.toml")
    consumer = Consumer(config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop)
    loop.close()
