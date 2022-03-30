import os, jwt, random, yagmail
from datetime import datetime
from datetime import timedelta


# get encryption key from environment variables for testing this is set in bootstrap
# todo - remove key from bootstrap to secure configuration
SECRET_KEY = os.getenv('SECRET_KEY', None)
EMAIL = os.getenv('EMAIL', None)
KEY = os.getenv('KEY', None)

OTPs = {}

def generateToken(userOTP, userEmail):
    """
    Generates authentication token

    :param: an allowed email for a user which hasn't registered yet
    :return: the authentication token or None if there is an exception
    """
    if (OTPs[userEmail]['otp'] != userOTP):
        raise ValueError
    if ((datetime.utcnow() - OTPs[userEmail]['iat']) > timedelta(hours=1)):
        raise ValueError
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

def authenticateEmail(userEmail):
    email = yagmail.SMTP(EMAIL, KEY)
    OTPs[userEmail] = {
            "otp": random.randint(100000, 999999),
            "iat": datetime.utcnow()
            }
    email.send(to=userEmail, subject="Your OTP for Loco", contents="Your one-time password is: " + str(OTPs[userEmail]['otp'])
        )
    return True
