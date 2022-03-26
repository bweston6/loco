from flask import Flask

from .api import api
from .web import web

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(web)
    return app
