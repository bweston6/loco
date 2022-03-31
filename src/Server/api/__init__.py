from flask import Blueprint
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
    """Updates the repository to the HEAD of the base branch, triggering a restart.
   
    :return: "ok" to indicate success.
    :rtype: String
    """
    system("git fetch; git reset origin/base --hard; git pull")
    return "ok"
