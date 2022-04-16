from . import api
from .. import database as db
from flask import jsonify
from flask import request
from mariadb import Error
import logging
import jwt
import json


@api.route("/getUsersFromGroup", methods=["POST"])
def getUsersFromGroup():
    """Returns the users from the selected group, provided that the ``email`` encoded in the ``token`` matches the ``hostEmail`` for the group.

    :<json str token: A valid *host* authentication token (see :http:post:`/api/createUser`)
    :<json str groupID: The ID of the group you want to get. Must be created by the user who is accessing this endpoint

    :>json str[] emails: The emails of everyone in the group
    :>json string error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if "token" in requestData and "groupID" in requestData:
            queryValidate = (
                "SELECT EXISTS ( "
                "SELECT * "
                "FROM users "
                "WHERE token = ? "
                "LIMIT 1)"
            )
            queryUsers = "SELECT emails " "FROM `groups` " "WHERE group_ID = ? "
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(queryValidate, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                cursor.execute(queryUsers, (requestData["groupID"],))
                user = cursor.fetchone()
                user = {"emails": json.loads(user[0])}
                return jsonify(user), 200
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
