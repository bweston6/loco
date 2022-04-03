# being worked on by Ben
# todo - remove this message

from . import api
from .. import auth, database as db
from flask import jsonify, request
from mariadb import Error
import logging, jwt

@api.route('/getUser', methods=['POST'])
def getUser():
    """Gets a user from the database via their email

    :<json str token: A valid authentication token (see :http:post:`/api/createUser`)
    :<json str email: The email of the user you want to get

    :>json str fullName: The full name of the user
    :>json str email: The email of the user
    :>json bool hostFlag: A flag to represent whether this is an attendee or host account

    :statuscode 200: Operation completed successfully
    :statuscode 400: JSON parameters are missing
    :statuscode 401: Invalid authentication token
    :statuscode 500: Server database error
    """
    try:
        requestData = request.get_json()
        if 'token' in requestData and 'email' in requestData:
            # validating token
            query1 = ("""SELECT EXISTS (
                SELECT *
                FROM users
                WHERE token = ?
                LIMIT 1
            )
            """)
            # finding user information from primary key
            query2 = ("""SELECT full_name, email, host_flag
                FROM users
                WHERE email = ?
            """)
            conn = db.openConnection()
            cursor = conn.cursor()
            cursor.execute(query1, (requestData['token'], ))
            tokenValid = cursor.fetchone()[0]
            if tokenValid == 1:
                cursor.execute(query2, (requestData['email'], ))
                user = cursor.fetchone()
                user = {"fullName": user[0],
                        "email": user[1],
                        "hostFlag": bool(user[2])
                        }
                return jsonify(user)
            else:
                db.closeConnection(conn)
                raise jwt.InvalidTokenError
        else:
            return jsonify(error='missing parameters'), 400
    except jwt.InvalidTokenError as e:
        logging.info('User query attempted with invalid token')
        return jsonify(error='invalid token'), 401
    except Error as e:
        logging.error(e)
        return jsonify(error='database error'), 500
