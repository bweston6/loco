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

    :returns: The generated authentication token or an error page if there has been an error.
    """
    try:
        conn = db.openConnection()
        requestData = request.get_json()
        if 'OTP' in requestData and 'fullName' in requestData and 'email' in requestData and 'hostFlag' in requestData:
            token = auth.generateToken(int(requestData['OTP']), requestData['email'])
        else: 
            return jsonify(error='missing parameters'), 400
        db.closeConnection(conn)
        return jsonify(token)
    except KeyError as e:
        return jsonify(error='email not authenticated'), 400
    except ValueError as e:
        return jsonify(error='invalid OTP'), 400
    except Error as e:
        return jsonify(error='database error'), 500

#   "outline for the data insertion data can be of any type"
#   addUser = ("INSERT INTO users "
#              "(first_name, email, auth, host_flag) "
#              "VALUES (%s, %s, %s, %s)")
#   dataUser = (data, data, data, data)
#   cursor.execute(addUser, dataUser)
#   conn.commit()
