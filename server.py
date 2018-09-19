
from flask import Flask
from flask import request
from main import create_map
from map import Map
import time
import random
import sys
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def homepage():
    seed = request.args.get('seed', None)
    draw_mode = request.args.get('draw_mode', 'map')
    create_map(seed=seed, draw_mode=draw_mode)

    return '<img src="static/latest_screenshot.png?{}">'.format(time.time())


@app.route('/api/create-map')
def map_api():
    map_width = int(request.args.get('width', 32))
    seed = request.args.get('seed', str(random.randint(0, sys.maxsize)))
    map = Map(map_width, seed)
    map.create()

    return jsonify({'map': map.to_dict()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
