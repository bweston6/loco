# Gunan
# mans on it still

from . import api
from .. import database as db
from flask import jsonify
from flask import request
from mariadb import Error
import logging


@api.route("/getAttendance", methods=["POST"])
def getAttendance():
    """Returns attendance for a particular ``email`` and ``eventID`` combination. Hosts can see any user's attendance but attendees can only see their own attendance. If an attendee is not enrolled in the event an error message is returned.

    :<json str token: A valid host authentication token, or a token that matches ``email`` (see :http:post:`/api/createUser`)
    :<json str email: The ``email`` of the attendee you are looking for
    :<json str eventID: The ``eventID`` of the event you are looking for

    :>json bool attended: A boolean indicating whether an attendee attended an event
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
            q1 = """ SELECT attendance_flag
                FROM attendance
                WHERE email = ?
            """
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(q1, (requestData["email"],))
            attendance = cursor.fetchone()[0]

            return attendance

        else:
            return jsonify(error="missing parameters"), 400

    except Error as e:
        logging.error(e)
        return jsonify(error="database error"), 500
