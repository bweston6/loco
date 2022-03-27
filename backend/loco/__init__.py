from flask import Flask

import loco.database as db
from .api import api
from .web import web

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
