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
    """Generates authentication token provided that ``userOTP`` and ``userEmail`` are valid. This is checked using the ``OTPs`` dictionary (see :func:`authenticateEmail`). ``userOTP`` must be under 1 hour old and ``userOTP`` and ``userEmail`` must match in the dictionary.

    :param userOTP: The user's one time password
    :type userOTP: str
    :param userEmail: The user's email
    :type userEmail: str
    :raises ValueError: If the ``userOTP`` or ``userEmail`` are invalid, or don't match
    :return: An authentication token encoding the issued time and ``userEmail``
    :rtype: str
    """
    if (OTPs[userEmail]['otp'] != userOTP):
        raise ValueError
    if ((datetime.utcnow() - OTPs[userEmail]['iat']) > timedelta(hours=1)):
        raise ValueError
    # delete OTP now it has been used
    del OTPs[userEmail]
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
    """Decodes ``token``

    :param token: The token to decode
    :type token: str
    :raises jwt.InvalidTokenError: If ``token`` is invalid
    :return: The subject field of the token (see ``userEmail`` in :func:`generateToken`)
    :rtype: str
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload['sub'] # subject (userEmail)

def authenticateEmail(userEmail):
    """Sends a one time password to the email ``userEmail``. The combination of OTP, ``userEmail`` and the issued time are saved in the dictionary ``OTPs``.

    :param userEmail: The email to send the OTP to
    :type userEmail: str
    :return: True when the action is complete
    :rtype: bool
    """
    email = yagmail.SMTP(EMAIL, KEY)
    OTPs[userEmail] = {
            "otp": random.randint(100000, 999999),
            "iat": datetime.utcnow()
            }
    email.send(to=userEmail, subject="Your OTP for Loco", contents=str(OTPs[userEmail]['otp']) + " is your one-time password.")
    return True
