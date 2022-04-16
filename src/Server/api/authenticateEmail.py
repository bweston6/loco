from flask import jsonify
from flask import request
from . import api
from .. import auth


@api.route("/authenticateEmail", methods=["POST"])
def authenticateEmail():
    """Emails a user with an one time password using :obj:`Server.auth.authenticateEmail`.

    :<json string email: The email that you want to authenticate

    :>json bool success: Indicates that the email has been sent to ``email``
    :>json string error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    """
    requestData = request.get_json()
    if "email" in requestData:
        auth.authenticateEmail(requestData["email"])
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, error="missing parameters"), 400
