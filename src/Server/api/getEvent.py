from Server import auth, database as db
from flask import Blueprint
from flask import jsonify
from flask import request
from mariadb import Error
import jwt
import logging
import simplejson as sjson

getEventBP = Blueprint("getEvent", __name__)


@getEventBP.route("/getEvent", methods=["POST"])
def getEvent():
    """Retrieves the details of an event identified by ``eventID``. The attendees of an event will only be returned if a *host* ``token`` is used.

    :<json str token: A valid authentication token (see :http:post:`/api/createUser`)
    :<json number eventId: The ``eventID`` you want to get the details of

    :>json int eventID: The group's unique ID
    :>json string eventName: The group's name
    :>json int startTime: The date and time the event is expected to start as a Unix timestamp: (``1649329200`` for ``Thu Apr 07 2022 11:00:00 UTC+0000``)
    :>json int duration: The duration of an event in Unix millis since the ``startTime``
    :>json float locationLong: The longitudinal coordinate of an event's location as a fixed point decimal in the format: ``±99.999999``
    :>json float locationLat: The latitudinal coordinate of an event's location as a fixed point decimal in the format: ``±999.999999``
    :>json int radius: The radius around an event's coordinates where attendance is accepted in meters
    :>json str description: A description of the event for users. Maximum of 1000 characters
    :>json str hostEmail: The email of the host of the event. This email must have an account created by using :http:post:`/api/createUser`
    :>json string[] emails: optional All the users emails that are in the group. Only returned if a *host* ``token`` is provided
    :>json string error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if "eventID" in requestData and "token" in requestData:
            # validation of token
            query1 = """SELECT EXISTS (
                SELECT *
                FROM users
                WHERE token = ?
                LIMIT 1
            )
            """

            query2 = """SELECT *
                FROM events
                WHERE event_ID = ?
            """

            query3 = """SELECT email
                FROM attendance
                WHERE event_ID = ?
            """

            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(query1, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]

            if tokenValid == 1:
                cursor.execute(query2, (requestData["eventID"],))
                event = cursor.fetchone()
                cursor.execute(query3, (requestData["eventID"],))
                attendees = cursor.fetchall()
                if event is None:
                    return jsonify(error="invalid event ID"), 400
                if auth.checkHostToken(requestData["token"], cursor):
                    # if requesting host
                    event = {
                        "eventID": event[0],
                        "eventName": event[1],
                        "startTime": event[2],
                        "duration": event[3],
                        "locationLat": event[4],
                        "locationLong": event[5],
                        "radius": event[6],
                        "description": event[7],
                        "hostEmail": event[8],
                        "emails": attendees,
                    }
                else:
                    # if requesting attendee
                    event = {
                        "eventID": event[0],
                        "eventName": event[1],
                        "startTime": event[2],
                        "duration": event[3],
                        "locationLat": event[4],
                        "locationLong": event[5],
                        "radius": event[6],
                        "description": event[7],
                        "hostEmail": event[8],
                    }
                return (
                    sjson.dumps(event),
                    200,
                    {"Content-Type": "application/json; charset=utf-8"},
                )
            else:
                db.closeConnection(conn)
                raise jwt.InvalidTokenError

        else:
            return jsonify(error="missing parameters"), 400

    except jwt.InvalidTokenError:
        logging.info("User query attempted with invalid token")
        return jsonify(error="invalid token"), 401
    except Error as e:
        logging.error(e)
        db.closeConnection(conn)
        return jsonify(error="database error"), 500
