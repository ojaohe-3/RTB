
import toml
import asyncio
from pymongo import MongoClient
from quart import Quart, jsonify
from quart import render_template
import requests

app = Quart(__name__)


@app.route('/')
async def index():
    return await render_template("konva.html", info={"title": "Construction Test Site",
                                                     "services": [{"title": "Actors", "id": 0},
                                                                  {"title": "Activites", "id": 1},
                                                                  {"title": "Structures", "id": 2}]})
@app.route('/data')
async def sendRequesterData():
    r = requests.get("http://127.0.0.1:5001/get-actor-data")
    return jsonify(r.json())

@app.route('/data/structures')
async def sendStructures():
    print("got a structure request")
    r = requests.get("http://127.0.0.1:5001/get-structure-data")
    return jsonify(r.json())

def getData(conf, loop):
    return ''

if __name__ == '__main__':
    app.run(debug=True)
    config = toml.load("config.toml")
    loop = asyncio.get_event_loop()
    loop.run_forever()