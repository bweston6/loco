# being worked on by Ben
# todo - remove this message

from flask import jsonify, request
from mariadb import Error
from loco.api import api
import loco.database as db
import loco.auth as auth

@api.route('/createUser', methods=['POST'])
def createUser():
    """
    Creates a user, generates an authentication token and adds the information to the database.

    :returns: The token with a HTTP sucess code, or an error with appropriate HTTP error code.
    """
    try:
        requestData = request.get_json()
        if 'OTP' in requestData and 'fullName' in requestData and 'email' in requestData and 'hostFlag' in requestData:
            token = auth.generateToken(int(requestData['OTP']), requestData['email'])
            conn = db.openConnection()
            cursor = conn.cursor()
            addUser = ("""REPLACE INTO users (
                    full_name,
                    email,
                    token,
                    host_flag
                )
                VALUES (?, ?, ?, ?)"""
            )
            userData = (
                requestData['fullName'],
                requestData['email'],
                token,
                requestData['hostFlag']
            )
            print(token)
            cursor.execute(addUser, userData)
            conn.commit()
            db.closeConnection(conn)
            return jsonify(token=token), 200
        else: 
            return jsonify(error='missing parameters'), 400
    except KeyError as e:
        return jsonify(error='email not authenticated'), 401
    except ValueError as e:
        return jsonify(error='invalid OTP'), 401
#    except Error as e:
#        return jsonify(error='database error'), 500
