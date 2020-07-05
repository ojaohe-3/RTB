from src.ConsumerActor import ConsumerActor
import toml
import asyncio
from pymongo import MongoClient
from flask import Flask, jsonify

app = Flask(__name__)

config = toml.load("config.toml")

client = MongoClient(f"mongodb://{config['MongoDB']['host']}:{config['MongoDB']['port']}")
db = client['rtb']
collection = db['Actors']

@app.route('/')
def index():
    return "Hello Worlds"


@app.route('/get-actor-data', methods=['GET'])
def sendRequesterData():

    # todo authentication
    msg = collection.find()
    results = []
    for result in msg:
        results.append({'Name': result['Name'],
                        'Position': result['position'],
                        'Shape': result['shape'],
                        'Color': result['color']})

    return jsonify(results)


@app.route('/data/structures')
async def sendStructures():
    return "hello world"


async def getData(conf, loop):
    return ''


loop = asyncio.get_event_loop()

if __name__ == '__main__':
    app.run(host="localhost", port="5001", debug=True)

