from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

import loco.api.createEvent
import loco.api.createGroup
import loco.api.createUser
import loco.api.getAttendance
import loco.api.getEvent
import loco.api.getUser
import loco.api.getUsersFromGroup
import loco.api.setAttendance

@api.route("/webhook", methods=["POST"])
def webook():
    """
    Updates the repository to the HEAD of the base branch, triggering a restart.
    
    :returns: The string "ok" to indicate success for GitHub.       
    """
    system("export GIT_SSH_COMMAND='ssh -i /home/loco/.ssh/loco -o IdentitiesOnly=yes'; git fetch; git reset origin/base --hard; git pull")
    return "ok"
