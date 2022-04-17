from flask import Blueprint
from flask import request
from os import system
from threading import Thread


api = Blueprint("api", __name__, url_prefix="/api")

from . import authenticateEmail
from . import createEvent
from . import createGroup
from . import createUser
from . import getAttendance
from . import getEvent
from . import getUser
from . import getUsersFromGroup
from . import setAttendance


@api.route("/webhook", methods=["POST"])
def webook():
    """Asyncronously calls :obj:`Server.api.update` triggering a restart, provided that tests pass.

    :<json str action: The current status of the workflow
    :<json str workflow.name: The name of the workflow

    :return: A status message to indicate the action taken
    :rtype: str

    :status 200: Request ignored successfully
    :status 201: Update to HEAD started
    """
    requestData = request.get_json()
    if (
        "conclusion" in requestData["workflow_run"]
        and "name" in requestData["workflow_run"]
        and requestData["workflow_run"]["conclusion"] == "success"
        and requestData["workflow_run"]["name"] == "server_tests"
    ):
        Thread(target=compileDocs).start()
        Thread(target=update).start()
        return "updated to HEAD", 201
    return "request ignored", 200


def update():
    """Updates the repository to the HEAD of the base branch and rebuilds the documentation.

    :return: Confirmation that the task completed successfully
    :rtype: bool
    """
    system("git fetch; git reset origin/base --hard; git pull --ff-only")
    return True


def compileDocs():
    system("make -C ../docs clean; make -C ../docs html latexpdf")
    return True
