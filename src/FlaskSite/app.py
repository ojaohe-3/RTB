from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/config', methods="POST")
def postConfigs():
    return ''


@app.route('/data', methods="GET")
def sendData():
    # todo authentication
    # todo get data from socket if available
    # todo generate json and send to requester
    return ''


async def getData(conf, loop):
    return ''


if __name__ == '__main__':
    app.run()
