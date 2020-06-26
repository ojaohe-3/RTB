from quart import Quart
from quart import render_template
import asyncio




app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template("konva.html",info={"title":"Construction Test Site"})

@app.route('/data')
async def sendRequesterData():
    print("got a data request")
    # todo authentication
    # todo get data from socket if available
    # todo generate json and send to requester



async def getData(conf, loop):
    return ''


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run()
