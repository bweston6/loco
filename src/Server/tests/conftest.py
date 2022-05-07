from Server import auth
from Server import create_app
from Server.auth import OTPs
import Server.database as db
import pytest


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
    auth.authenticateEmail(hostEmail)
    return OTPs[hostEmail]["otp"]


@pytest.fixture()
def attendeeOTP(attendeeEmail):
    auth.authenticateEmail(attendeeEmail)
    return OTPs[attendeeEmail]["otp"]


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
