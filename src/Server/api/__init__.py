from flask import Blueprint, request
from os import system

api = Blueprint('api', __name__, url_prefix='/api')

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
    """Updates the repository to the HEAD of the base branch triggering a restart, provided that tests pass.
    :<json str action: The current status of the workflow
    :<json str workflow.name: The name of the workflow

    :return: A status message to indicate the action taken
    :rtype: str

    :status 200: Request completed or ignored successfully
    """
    requestData = request.get_json()
    if requestData['action'] == "completed" and requestData['workflow']['name'] == "Testing":
        system("git fetch; git reset origin/base --hard; git pull")
        return "updated to HEAD", 200
    return "request ignored", 200
