# Gunan

from flask import Blueprint
from Server import database as db
from flask import jsonify
from flask import request
from mariadb import Error
import jwt
import logging

setAttendanceBP = Blueprint("setAttendance", __name__)


@setAttendanceBP.route("/setAttendance", methods=["POST"])
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
            and "attended" in requestData
        ):
            queryValidate = """SELECT EXISTS (
                    SELECT *
                    FROM users
                    WHERE token = ? AND host_flag IS TRUE
                    LIMIT 1)"""

            validateID = """SELECT EXISTS (
                    SELECT *
                    FROM events
                    WHERE event_ID = ?
                    LIMIT 1)"""

            q1 = """REPLACE INTO attendance
                VALUES (?, ?, ?)
            """
            attendanceData = (
                requestData["email"],
                requestData["eventID"],
                requestData["attended"],
            )
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(queryValidate, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                cursor.execute(validateID, (requestData["eventID"],))
                eventIDValid = cursor.fetchone()[0]
                if eventIDValid  == 1:
                    cursor.execute(q1, attendanceData)
                    conn.commit()
                    db.closeConnection(conn)
                    return jsonify(success=True), 200
                else:
                    db.closeConnection(conn)
                    logging.info("Attendance query attempted with non-existent ID")
                    return jsonify(error="invalid eventID"), 400
            else:
                db.closeConnection(conn)
                raise jwt.InvalidTokenError
        else:
            return jsonify(error="missing parameters"), 400
    except jwt.InvalidTokenError:
        logging.info("Attendance set attempted with invalid token")
        return jsonify(error="invalid token"), 401
    except Error as e:
        logging.error(e)
        db.closeConnection(conn)
        return jsonify(error="database error"), 500
