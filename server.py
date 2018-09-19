
from flask import Flask
from flask import request
from main import create_map
import time

app = Flask(__name__)


@app.route('/')
def homepage():
    seed = request.args.get('seed', None)
    draw_mode = request.args.get('draw_mode', 'map')
    create_map(seed=seed, draw_mode=draw_mode)

    return '<img src="static/latest_screenshot.png?{}">'.format(time.time())
