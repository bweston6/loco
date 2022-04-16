# being worked on by Ben
# todo - remove this message

from . import api
from .. import auth, database as db
from flask import jsonify
from flask import request
from mariadb import Error
import logging
import jwt


@api.route("/getUser", methods=["POST"])
def getUser():
    """When used on an attendee, this returns the user's details and a list of enrolled events. The enrolled ``eventIDs`` are only returned if the ``email`` matches the ``token`` or if a *host* ``token`` is used. When used on a host, this returns the host's details, list of created ``groupIDs`` and list of created ``eventIDs``. The host ``groupIDs`` and ``eventIDs`` are only returned if the ``email`` matches the ``token``. An error is returned if the ``email`` is not registered.

    :<json str token: A valid authentication token (see :http:post:`/api/createUser`)
    :<json str email: The email of the user you want to get

    :>json str fullName: The full name of the user
    :>json str email: The email of the user
    :>json bool hostFlag: A flag to represent whether this is an attendee or host account
    :>json int[] eventIDs: optional A list of created or enrolled events for the user. Only shown if the user is authenticated to see them
    :>json int[] groupIDs: optional A list of created groups. Only shown if the user is authenticated to see them
    :>json string error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing or invalid
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if "token" in requestData and "email" in requestData:
            # validating token
            query1 = """SELECT EXISTS (
                SELECT *
                FROM users
                WHERE token = ?
                LIMIT 1
            )
            """
            # finding user information from primary key
            query2 = """SELECT full_name, email, host_flag
                FROM users
                WHERE email = ?
            """
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(query1, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                cursor.execute(query2, (requestData["email"],))
                user = cursor.fetchone()
                # check if user exists
                if user is None:
                    return jsonify(error="email is not registered"), 400
                user = {
                    "fullName": user[0],
                    "email": user[1],
                    "hostFlag": bool(user[2]),
                }
                if auth.checkHostEmail(requestData["email"], cursor):
                    # if requesting host
                    # if email matches token then add extra info
                    if requestData["email"] == auth.decodeToken(requestData["token"]):
                        # find all groups this host has made
                        query3 = """SELECT group_ID
                            FROM `groups`
                            WHERE hostEmail = ?
                        """
                        # find all events this host has made
                        query4 = """SELECT event_ID
                            FROM events
                            WHERE hostEmail = ?
                        """
                        cursor.execute(query3, (requestData["email"],))
                        user["groupIDs"] = cursor.fetchall()
                        cursor.execute(query4, (requestData["email"],))
                        user["eventIDs"] = cursor.fetchall()
                else:
                    # if requesting attendee
                    # add eventIDs if email matches token or host
                    if requestData["email"] == auth.decodeToken(
                        requestData["token"]
                    ) or auth.checkHostToken(requestData["token"], cursor):
                        query5 = """
                            SELECT event_ID
                            FROM attendance
                            WHERE email = ?
                        """
                        cursor.execute(query5, (requestData["email"],))
                        user["eventIDs"] = cursor.fetchall()

                return jsonify(user)
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
