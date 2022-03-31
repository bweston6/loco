from flask import Flask

import logging
from . import database as db
from .api import api
from .web import web

# todo - set to WARNING for release
logging.basicConfig(level=logging.INFO)

def create_app():
    """
    Ensures database tables are created, creates the main flask app and registers blueprints to the main app.
    :returns: the main flask app
    """
    conn = db.openConnection()
    db.createTables(conn.cursor())
    db.closeConnection(conn)
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(web)
    return app
