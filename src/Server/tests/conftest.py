from Server import auth
from Server import create_app
from Server.auth import OTPs
from datetime import datetime
from freezegun import freeze_time
import Server.database as db
import jwt
import os
import pytest
import random


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def hostEmail():
    return "drop@bweston.uk"


@pytest.fixture()
def attendeeEmail():
    return "dropdrop@bweston.uk"


@pytest.fixture()
def hostName():
    return "Host Smith"


@pytest.fixture()
def attendeeName():
    return "Attendee Smith"


@pytest.fixture()
def hostOTP(hostEmail):
    OTPs[hostEmail] = {"otp": random.randint(100000, 999999), "iat": datetime.utcnow()}
    return OTPs[hostEmail]["otp"]


@pytest.fixture()
def attendeeOTP(attendeeEmail):
    OTPs[attendeeEmail] = {
        "otp": random.randint(100000, 999999),
        "iat": datetime.utcnow(),
    }
    return OTPs[attendeeEmail]["otp"]


@pytest.fixture()
@freeze_time("2000-09-06")
def hostToken(hostEmail, SECRET_KEY):
    return jwt.encode(
        {"iat": datetime.utcnow(), "sub": hostEmail}, SECRET_KEY, algorithm="HS256"
    )


@pytest.fixture()
@freeze_time("2000-09-06")
def attendeeToken(attendeeEmail, SECRET_KEY):
    return jwt.encode(
        {"iat": datetime.utcnow(), "sub": attendeeEmail}, SECRET_KEY, algorithm="HS256"
    )


@pytest.fixture()
def SECRET_KEY():
    return os.getenv("SECRET_KEY", None)


@pytest.fixture()
def attendee(attendeeName, attendeeEmail, attendeeOTP):
    conn = db.openConnection()
    cursor = conn.cursor()
    user = {"name": attendeeName, "email": attendeeEmail, "hostFlag": False}
    user["token"] = auth.generateToken(attendeeOTP, attendeeEmail)
    addUser = """REPLACE INTO users (
        full_name,
        email,
        token,
        host_flag
        )
        VALUES (?, ?, ?, ?)"""
    userData = (user["name"], user["email"], user["token"], user["hostFlag"])
    cursor.execute(addUser, userData)
    conn.commit()
    db.closeConnection(conn)
    return user


@pytest.fixture()
def host(hostName, hostEmail, hostOTP):
    conn = db.openConnection()
    cursor = conn.cursor()
    user = {"name": hostName, "email": hostEmail, "hostFlag": True}
    user["token"] = auth.generateToken(hostOTP, hostEmail)
    addUser = """REPLACE INTO users (
        full_name,
        email,
        token,
        host_flag
        )
        VALUES (?, ?, ?, ?)"""
    userData = (user["name"], user["email"], user["token"], user["hostFlag"])
    cursor.execute(addUser, userData)
    conn.commit()
    db.closeConnection(conn)
    return user


@pytest.fixture()
def conn():
    connection = db.openConnection()
    cursor = connection.cursor()
    yield connection
    db.closeConnection(connection)
