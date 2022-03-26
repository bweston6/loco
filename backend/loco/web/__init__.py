from flask import Blueprint

web = Blueprint('web', __name__, static_folder='static')

@web.route('/')
def index():
    return web.send_static_file('index.html')