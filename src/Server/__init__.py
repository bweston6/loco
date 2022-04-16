from flask import Flask

import logging
from . import database as db
from .api import api
from .web import web

# todo - set to WARNING for release
logging.basicConfig(level=logging.INFO)


def create_app():
    """Creates the database tables using :obj:`Server.database.createTables`, creates the flask instance ``app`` and registers all blueprints under that instance.

    :return: The flask instance ``app``
    :rtype: flask.app.Flask
    """
    conn = db.openConnection()
    db.createTables(conn.cursor())
    db.closeConnection(conn)
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_blueprint(web)
    return app


# create public varaible for hupper
app = create_app()
