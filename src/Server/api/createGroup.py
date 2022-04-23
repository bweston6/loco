# being worked on by Leon

from . import api
from .. import database as db
from flask import jsonify
from flask import request
from mariadb import Error
import logging
import jwt
import json


@api.route("/createGroup", methods=["POST"])
def createGroup():
    """Creates a group with a set of emails to allow for quicker repeating event creation.

    :<json str token: A valid host authentication token (see :http:post:`/api/createUser`)
    :<json int groupID: optional The group's unique ID if you want to change an existing group
    :<json string groupName: The group's name. Maximum of 50 characters
    :<json string[] emails: All the user's emails that are in the group

    :>json int groupID: The ``groupID`` of the created or modified group
    :>json str error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        requestData["emails"] = json.dumps(requestData["emails"])
        if (
            "token" in requestData
            and "groupName" in requestData
            and "emails" in requestData
        ):
            queryValidate = (
                "SELECT EXISTS ( "
                "SELECT * "
                "FROM users "
                "WHERE token = ? "
                "LIMIT 1)"
            )
            getHostEmail = "SELECT email " "FROM users " "WHERE token = ? "
            groupIDExists = False
            if "groupID" in requestData:
                addGroup = (
                    "REPLACE INTO `groups` ("
                    "group_ID, "
                    "group_name, "
                    "hostEmail, "
                    "emails) "
                    "VALUES (?, ?, ?, ?)"
                )
                groupIDExists = True
            else:
                addGroup = (
                    "INSERT INTO `groups` ("
                    "group_name, "
                    "hostEmail, "
                    "emails) "
                    "VALUES (?, ?, ?)"
                )
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(queryValidate, (requestData["token"],))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                cursor.execute(getHostEmail, (requestData["token"],))
                if groupIDExists:
                    groupData = (
                        requestData["groupID"],
                        requestData["groupName"],
                        cursor.fetchone()[0],
                        requestData["emails"],
                    )
                else:
                    groupData = (
                        requestData["groupName"],
                        cursor.fetchone()[0],
                        requestData["emails"],
                    )
                cursor.execute(addGroup, groupData)
                conn.commit()
                db.closeConnection(conn)
                return jsonify(groupData), 200
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
