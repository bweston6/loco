from Server import auth
from freezegun import freeze_time
import Server.database as db
import datetime
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", None)


@freeze_time("2000-09-06")
def test_generateToken(hostOTP, hostEmail):
    payload = jwt.decode(
        auth.generateToken(hostOTP, hostEmail), SECRET_KEY, algorithms=["HS256"]
    )
    print(type(payload["iat"]))
    print(payload["iat"])
    print(payload["sub"])
    assert payload["iat"] == datetime.datetime(2000, 9, 6).timestamp()
    assert payload["sub"] == hostEmail


def test_decodeToken(host):
    assert auth.decodeToken(host["token"]) == host["email"]


def test_authenticateEmail(hostEmail):
    assert auth.authenticateEmail(hostEmail) == True


def test_checkHostEmail(host, attendee, conn):
    cursor = conn.cursor()
    assert auth.checkHostEmail(host["email"], cursor) == True
    assert auth.checkHostEmail(attendee["email"], cursor) == False


def test_checkHostToken(host, attendee, conn):
    cursor = conn.cursor()
    assert auth.checkHostToken(host["token"], cursor) == True
    assert auth.checkHostToken(attendee["token"], cursor) == False
