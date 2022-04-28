from Server.api.authenticateEmail import authenticateEmailBP
from Server.api.createEvent import createEventBP
from Server.api.createGroup import createGroupBP
from Server.api.createUser import createUserBP
from Server.api.getAttendance import getAttendanceBP
from Server.api.getEvent import getEventBP
from Server.api.getUser import getUserBP
from Server.api.getUsersFromGroup import getUsersFromGroupBP
from Server.api.setAttendance import setAttendanceBP
from flask import Blueprint
from flask import request
from os import system
from threading import Thread

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(authenticateEmailBP)
api.register_blueprint(createEventBP)
api.register_blueprint(createGroupBP)
api.register_blueprint(createUserBP)
api.register_blueprint(getAttendanceBP)
api.register_blueprint(getEventBP)
api.register_blueprint(getUserBP)
api.register_blueprint(getUsersFromGroupBP)
api.register_blueprint(setAttendanceBP)


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
