# being worked on by Ben
# todo - remove this message

from flask import abort, jsonify, request
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
        db.createTables(conn.cursor())
        requestData = request.get_json()
        if 'fullName' in requestData and 'email' in requestData and 'hostFlag' in requestData:
            token = auth.generateToken(requestData['email'])
        else: 
            return jsonify(error='missing parameters'), 400
        db.closeConnection(conn)
        return jsonify(token)
    except Error:
        return jsonify(error='database error'), 500
