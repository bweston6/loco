from flask import Blueprint

web = Blueprint('web', __name__, static_folder='_static')

@web.route('/')
def index():
    """
    Description

    :returns: 
    """
    return web.send_static_file('index.html')