from flask import jsonify, request
from mariadb import Error
from loco.api import api
import loco.auth as auth

@api.route('/authenticateEmail', methods=['POST'])
def authenticateEmail():
    """
    Emails a user with an one time passsword

    :returns: A HTTP success code.
    """
    requestData = request.get_json()
    if 'email' in requestData:
        auth.authenticateEmail(requestData['email'])
        return jsonify("success"), 200
    else: 
        return jsonify(error='missing parameters'), 400
