# Gunan
# incomplete still

from . import api
from .. import database as db
from flask import jsonify
from flask import request
from mariadb import Error
import logging


@api.route("/setAttendance", methods=["POST"])
def setAttendance():
    """Sets the enrolment status and attendance for a particular ``email`` and ``eventID``. Only successful if the ``email`` matches the ``token`` or if a *host* ``token`` is used.

    :<json str token: A valid host authentication token, or a token that matches ``email`` (see :http:post:`/api/createUser`)
    :<json str email: The ``email`` of the attendee you want to enrol or mark as attended
    :<json str eventID: The ``eventID`` of the event this is regarding
    :<json bool attended: The attendance status for this ``eventID`` and ``email``. Must be set to ``false`` to register an attendee, or ``true`` to mark an attendee as attended.

    :>json bool success: Indicates that the operation is successful ``email``
    :>json string error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing or invalid
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if (
            "token" in requestData
            and "email" in requestData
            and "eventID" in requestData
        ):
            q1 = """ UPDATE attendance
                SET attendance_flag = "True"
                WHERE eventID = ? AND email = ?
            """
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(
                q1,
                (
                    requestData["eventID"],
                    requestData["email"],
                ),
            )

        else:
            return jsonify(error="missing parameters"), 400

    except Error as e:
        logging.error(e)
        return jsonify(error="database error"), 500
