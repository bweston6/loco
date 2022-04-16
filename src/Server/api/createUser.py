# being worked on by Ben
# todo - remove this message

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging


@api.route("/createUser", methods=["POST"])
def createUser():
    """Creates a user, generates an authentication token and adds the information to the database.

    :<json string OTP: The one time password associated with the ``email`` you want to register. This is received by calling :http:post:`/api/authenticateEmail`
    :<json str fullName: The full name of the user you want to register
    :<json str email: The email you want to register under (must have a registered OTP using :http:post:`/api/authenticateEmail`)
    :<json bool hostFlag: Defines where the user is a host or an attendee

    :>json str token: The authentication ``token`` for the new user
    :>json str error: optional An error message if the action cannot complete

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: JSON authentication parameters are invalid, see ``error``
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if (
            "OTP" in requestData
            and "fullName" in requestData
            and "email" in requestData
            and "hostFlag" in requestData
        ):
            token = auth.generateToken(int(requestData["OTP"]), requestData["email"])
            conn = db.openConnection()
            cursor = conn.cursor()
            findExistingUser = """SELECT EXISTS (
                SELECT *
                FROM users
                WHERE email = ?
                LIMIT 1
            )
            """
            cursor.execute(findExistingUser, (requestData["email"],))
            # test if user exists
            userExists = cursor.fetchone()[0]
            if userExists == 1:
                updateUser = """UPDATE users
                    SET full_name = ?,
                        token = ?,
                        host_flag = ?
                    WHERE email = ?"""
                userData = (
                    requestData["fullName"],
                    token,
                    requestData["hostFlag"],
                    requestData["email"],
                )
                cursor.execute(updateUser, userData)
            else:
                addUser = """REPLACE INTO users (
                        full_name,
                        email,
                        token,
                        host_flag
                    )
                    VALUES (?, ?, ?, ?)"""
                userData = (
                    requestData["fullName"],
                    requestData["email"],
                    token,
                    requestData["hostFlag"],
                )
                cursor.execute(addUser, userData)
            conn.commit()
            db.closeConnection(conn)
            return jsonify(token=token), 200
        else:
            return jsonify(error="missing parameters"), 400
    except KeyError:
        logging.info(
            requestData["email"]
            + " tried to create a user before authenticating their email."
        )
        return jsonify(error="email not authenticated"), 401
    except ValueError:
        logging.info(
            requestData["email"] + " tried to create a user with the wrong OTP."
        )
        return jsonify(error="invalid OTP"), 401
    except Error as e:
        logging.error(e)
        return jsonify(error="database error"), 500
