import os, jwt
from datetime import datetime

# get encryption key from environment variables for testing this is set in bootstrap
# todo - remove key from bootstrap to secure configuration
SECRET_KEY = os.getenv('SECRET_KEY', None)

def generateToken(userEmail):
    """
    Generates authentication token
	
    :param: an allowed email for a user which hasn't registered yet
    :return: the authentication token or None if there is an exception
    """
    payload = {
            'iat' : datetime.utcnow(), # issued at
            'sub' : userEmail # subject
            }
    return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
            )

def decodeToken(token):
    """
    Decodes a given authentication token
    :param: the authentication token to decode
    :return: the user's email or None if the token is invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except jwt.InvalidTokenError:
        return None
    else:
        return payload['sub'] # subject (userEmail)
