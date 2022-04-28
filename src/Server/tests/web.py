from flask import Blueprint

web = Blueprint("web", __name__, static_folder="_static")


@web.route("/")
def index():
    """Returns a home page for the project from the ``_static`` folder.

    :statuscode 200: Page returned successfully
    """
    return web.send_static_file("index.html"), 200
