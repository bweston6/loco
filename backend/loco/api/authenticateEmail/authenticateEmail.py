from flask import jsonify, request
from mariadb import Error
from loco.api import api
import loco.auth as auth

@api.route('/authenticateEmail', methods=['POST'])
def authenticateEmail():
    """
    Emails a user with an one time passsword

    :returns: A HTTP success code and success bool, or an error and 400 code if there are missing parameters.
    """
    requestData = request.get_json()
    if 'email' in requestData:
        auth.authenticateEmail(requestData['email'])
        return jsonify(success = true), 200
    else: 
        return jsonify(error = 'missing parameters'), 400
