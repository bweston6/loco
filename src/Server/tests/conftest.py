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
import json

"""Variable Fixtures"""


@pytest.fixture()
def SECRET_KEY():
    return os.getenv("SECRET_KEY", None)


"""Flask Fixtures"""


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


"""Database Fixtures"""


@pytest.fixture()
def conn():
    connection = db.openConnection()
    cursor = connection.cursor()
    dropAttendance = ("DROP TABLE IF EXISTS attendance"); cursor.execute(dropAttendance)
    dropEvents = ("DROP TABLE IF EXISTS events"); cursor.execute(dropEvents)
    dropGroups = ("DROP TABLE IF EXISTS `groups`"); cursor.execute(dropGroups)
    dropUsers = ("DROP TABLE IF EXISTS users"); cursor.execute(dropUsers)
    db.createTables(cursor)
    yield connection
    db.closeConnection(connection)


"""User Information Fixtures"""


@pytest.fixture()
def hostName():
    return "Host Smith"


@pytest.fixture()
def hostEmail():
    return "drop@bweston.uk"


@pytest.fixture()
def hostOTP(hostEmail):
    OTPs[hostEmail] = {"otp": random.randint(100000, 999999), "iat": datetime.utcnow()}
    return OTPs[hostEmail]["otp"]


@pytest.fixture()
@freeze_time("2000-09-06")
def hostToken(hostEmail, SECRET_KEY):
    return jwt.encode(
        {"iat": datetime.utcnow(), "sub": hostEmail}, SECRET_KEY, algorithm="HS256"
    )


@pytest.fixture()
def attendeeName():
    return "Attendee Smith"


@pytest.fixture()
def attendeeEmail():
    return "dropdrop@bweston.uk"


@pytest.fixture()
def attendeeOTP(attendeeEmail):
    OTPs[attendeeEmail] = {
        "otp": random.randint(100000, 999999),
        "iat": datetime.utcnow(),
    }
    return OTPs[attendeeEmail]["otp"]


@pytest.fixture()
@freeze_time("2000-09-06")
def attendeeToken(attendeeEmail, SECRET_KEY):
    return jwt.encode(
        {"iat": datetime.utcnow(), "sub": attendeeEmail}, SECRET_KEY, algorithm="HS256"
    )


@pytest.fixture()
def otherHostName():
    return "Other Host Smith"


@pytest.fixture()
def otherHostEmail():
    return "dropother@bweston.uk"


@pytest.fixture()
def otherHostOTP(otherHostEmail):
    OTPs[otherHostEmail] = {
        "otp": random.randint(100000, 999999),
        "iat": datetime.utcnow(),
    }
    return OTPs[otherHostEmail]["otp"]


@pytest.fixture()
def otherAttendeeName():
    return "Other Attendee Smith"


@pytest.fixture()
def otherAttendeeEmail():
    return "dropdropother@bweston.uk"


@pytest.fixture()
def otherAttendeeOTP(otherAttendeeEmail):
    OTPs[otherAttendeeEmail] = {
        "otp": random.randint(100000, 999999),
        "iat": datetime.utcnow(),
    }
    return OTPs[otherAttendeeEmail]["otp"]


"""User Creation Fixtures"""


@pytest.fixture()
def attendee(conn, attendeeName, attendeeEmail, attendeeOTP):
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
    return user


@pytest.fixture()
def host(conn, hostName, hostEmail, hostOTP):
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
    return user


@pytest.fixture()
def otherHost(conn, otherHostName, otherHostEmail, otherHostOTP):
    cursor = conn.cursor()
    user = {"name": otherHostName, "email": otherHostEmail, "hostFlag": True}
    user["token"] = auth.generateToken(otherHostOTP, otherHostEmail)
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
    return user


@pytest.fixture()
def otherAttendee(conn, otherAttendeeName, otherAttendeeEmail, otherAttendeeOTP):
    cursor = conn.cursor()
    user = {"name": otherAttendeeName, "email": otherAttendeeEmail, "hostFlag": False}
    user["token"] = auth.generateToken(otherAttendeeOTP, otherAttendeeEmail)
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
    return user

"""Event Creation Fixtures"""

@pytest.fixture()
def eventName():
    return "Lecture"

@pytest.fixture()
def startTime():
    return 1649329200

@pytest.fixture()
def duration():
    return 2

@pytest.fixture()
def locationLong():
    return Decimal('34.737273')

@pytest.fixture()
def locationLat():
    return Decimal('-22.124364')

@pytest.fixture()
def radius():
    return 200

@pytest.fixture()
def description():
    return "This is a Lecture."

@pytest.fixture()
def events(conn, eventName, startTime, duration, locationLat, locationLong, radius, description, hostEmail, emails):
    cursor = conn.cursor()
    event = {"eventName": eventName, "startTime": startTime, "duration": duration, "locationLat": locationLat, "locationLong": locationLong, "radius": radius, "description": description, "hostEmail": hostEmail}
    event["emails"] = json.dumps(emails)
    addEvent = (
        """INSERT INTO `events` (
        event_name, 
        start_time, 
        duration,
        latitude,
        longitude,
        radius,
        description,
        hostEmail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    )
    lastID = (
        "SELECT LAST_INSERT_ID()"
    )
    eventData = (
        event["eventName"],
        event["startTime"],
        event["duration"],
        event["locationLat"],
        event["locationLong"],
        event["radius"],
        event["description"],
        event["hostEmail"]
    )
    cursor.execute(addEvent, eventData)
    conn.commit()
    cursor.execute(lastID)
    event["emails"] = json.loads(event["emails"])
    event["eventID"] = cursor.fetchone()[0]
    return event

@pytest.fixture()
def otherEventName():
    return "notLecture"

@pytest.fixture()
def otherStartTime():
    return 1649329210

@pytest.fixture()
def otherDuration():
    return 3

@pytest.fixture()
def otherLocationLong():
    return Decimal('52.737273')

@pytest.fixture()
def otherLocationLat():
    return Decimal('12.124364')

@pytest.fixture()
def otherRadius():
    return 300

@pytest.fixture()
def otherDescription():
    return "This is not a Lecture."
"""Group Creation Fixtures"""

@pytest.fixture()
def groupName():
    return "COMP208"

@pytest.fixture()
def emails():
    return [
        "a@gmail.com",
        "b@gmail.com",
        "c@gmail.com",
        "d@gmail.com",
        "e@gmail.com",
        "f@gmail.com"
    ]

@pytest.fixture()
def group(conn, groupName, hostEmail, emails):
    cursor = conn.cursor()
    group = {"groupName": groupName, "hostEmail": hostEmail}
    group["emails"] = json.dumps(emails)
    addGroup = (
        "INSERT INTO `groups` ("
        "group_name, "
        "hostEmail, "
        "emails) "
        "VALUES (?, ?, ?)"
    )
    lastID = (
        "SELECT LAST_INSERT_ID()"
    )
    groupData = (
        group["groupName"],
        group["hostEmail"],
        group["emails"]
    )
    cursor.execute(addGroup, groupData)
    conn.commit()
    cursor.execute(lastID)
    group["emails"] = json.loads(group["emails"])
    group["groupID"] = cursor.fetchone()[0]
    return group

@pytest.fixture()
def otherGroupName():
    return "notCOMP208"

@pytest.fixture()
def otherEmails():
    return [
        "g@gmail.com",
        "h@gmail.com",
        "i@gmail.com",
        "j@gmail.com",
        "k@gmail.com",
        "l@gmail.com"
    ]