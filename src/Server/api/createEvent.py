# being worked on by Noushin

from flask import jsonify, request
from mariadb import Error
from . import api
from .. import auth
from .. import database as db
import logging
import jwt


@api.route("/createEvent", methods=["POST"])
def createEvent():
    """Creates an event, or updates an existing event if ``eventID`` is supplied.
    
    :<json str token: A valid *host* authentication token (see :http:post:`/api/createUser`)
    :<json int eventID: optional The `eventID` if you want to change an existing event
    :<json str eventName: The event name. Maximum of 100 characters
    :<json int startTime: The date and time the event is expected to start as a Unix timestamp: (``1649329200`` for ``Thu Apr 07 2022 11:00:00 UTC+0000``)
    :<json int duration: The duration of an event in Unix millis since the ``startTime``
    :<json float locationLong: The longitudinal coordinate of an event's location as a fixed point decimal in the format: ``±99.999999``
    :<json float locationLat: The latitudinal coordinate of an event's location as a fixed point decimal in the format: ``±999.999999``
    :<json int radius: The radius around an event's coordinates where attendance is accepted in meters
    :<json str description: A description of the event for users. Maximum of 1000 characters
    :<json str[] emails: An array of emails to enrol in the event
    
    :>json str token: The authentication ``token`` for the new event
    :>json string error: optional An error message if the action cannot complete
    
    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if (
            "token" in requestData
            and "eventName" in requestData
            and "startTime" in requestData
            and "duration" in requestData
            and "locationLong" in requestData
            and "locationLat" in requestData
            and "radius" in requestData
            and "description" in requestData
            and "emails" in requestData
        ):
            queryValidate = """SELECT EXISTS (
                    SELECT *
                    FROM users
                    WHERE token = ? AND host_flag IS TRUE
                    LIMIT 1)"""
            hostEmail = auth.decodeToken(requestData["token"])
            addEventOne = """REPLACE INTO events (
                event_ID,
                event_name,
                start_time,
                duration,
                latitude,
                longitude,
                radius,
                description,
                hostEmail
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            addEventTwo = """INSERT INTO events (
                event_name,
                start_time,
                duration,
                latitude,
                longitude,
                radius,
                description,
                hostEmail
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            eventDataTwo = (
                requestData["eventName"],
                requestData["startTime"],
                requestData["duration"],
                requestData["locationLat"],
                requestData["locationLong"],
                requestData["radius"],
                requestData["description"],
                hostEmail,
            )
            addAttendance = """REPLACE INTO attendance (
                    email,
                    event_ID,
                    attendance_flag
                )
                VALUES (?, ?, FALSE)"""
            getEventID = """SELECT event_ID
                FROM events
                WHERE event_name = ? AND start_time = ? AND duration = ? AND latitude = ? AND longitude = ? AND radius = ? AND description = ? AND hostEmail = ?"""
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(queryValidate, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                if "eventID" in requestData:
                    eventDataOne = (
                        requestData["eventID"],
                        requestData["eventName"],
                        requestData["startTime"],
                        requestData["duration"],
                        requestData["locationLat"],
                        requestData["locationLong"],
                        requestData["radius"],
                        requestData["description"],
                        hostEmail,
                    )
                    cursor.execute(addEventOne, eventDataOne)
                else:
                    cursor.execute(addEventTwo, eventDataTwo)
                cursor.execute(getEventID, eventDataTwo)
                eventID = cursor.fetchall()[0][0]
                emailArray = requestData["emails"]
                for email in emailArray:
                    attendanceData = (email, eventID)
                    cursor.execute(addAttendance, attendanceData)
                conn.commit()
                db.closeConnection(conn)
                return jsonify(eventID), 200
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
        return jsonify(error="database error"), 500
