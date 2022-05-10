from freezegun import freeze_time

@freeze_time("2000-09-06")

def test_createEvent_withoutID(eventName, startTime, duration, locationLong, locationLat, radius, description, emails, hostEmail, conn, client):
    token = ("""
        SELECT token
        FROM users
        WHERE hostEmail = ?"""
    )
    cursor.execute(event, hostEmail)
    tokenH = cursor.fetchall()[0][0]
    response = client.post(
        "/api/createEvent",
        json={
            "token": tokenH,
            "eventName": eventName,
            "startTime": startTime,
            "duration": duration,
            "locationLat": locationLat,
            "locationLong": locationLong,
            "radius": radius,
            "description": description,
            "emails": emails,
        },
    )
    eventID = (
        """SELECT LAST_INSERT_ID()"""
    )
    event = (
        """SELECT * 
        FROM events
        WHERE event_ID = ?"""
    )
    cursor = conn.cursor()
    cursor.execute(eventID)
    eventID = cursor.fetchone()
    cursor.execute(event, eventID)
    eventDB = cursor.fetchone()
    conn.commit()
    assert eventDB[0] == eventID
    assert eventDB[1] == eventName
    assert eventDB[2] == startTime
    assert eventDB[3] == duration
    assert eventDB[4] == locationLat
    assert eventDB[5] == locationLong
    assert eventDB[6] == radius
    assert eventDB[7] == description
    assert eventDB[8] == hostEmail

def test_createEvent_withID(events, otherEventName, otherStartTime, otherDuration, otherLocationLat, otherLocationLong, otherRadius, otherDescription, otherEmails, conn, client):
    token = ("""
        SELECT token
        FROM users
        WHERE hostEmail = ?"""
    )
    cursor.execute(event, hostEmail)
    tokenH = cursor.fetchall()[0][0]
    response = client.post(
        "/api/createEvent",
        json={
            "eventID": events["eventID"],
            "token": tokenH,
            "eventName": otherEventName,
            "startTime": otherStartTime,
            "duration": otherDuration,
            "locationLat": otherLocationLat,
            "locationLong": otherLocationLong,
            "radius": otherRadius,
            "description": otherDescription,
            "emails": otherEmails,
        },
    )
    event = (
        """SELECT *
        FROM events
        WHERE event_ID = ?"""
    )
    cursor = conn.cursor()
    cursor.execute(event, events["eventID"])
    eventDB = cursor.fetchone()
    conn.commit()
    assert eventDB[0] == events["eventID"]
    assert eventDB[1] == otherEventName
    assert eventDB[2] == otherStartTime
    assert eventDB[3] == otherDuration
    assert eventDB[4] == otherLocationLat
    assert eventDB[5] == otherLocationLong
    assert eventDB[6] == otherRadius
    assert eventDB[7] == otherDescription
    assert eventDB[8] == events["hostEmail"]

def test_createEvent_missingParameters(client):
    response = client.post(
        "/api/createEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_createEvent_invalidToken(eventName, startTime, duration, locationLat, locationLong, radius, description, emails, host, client):
    response = client.post(
        "/api/createEvent",
        json={
            "token": "idk",
            "eventName": eventName,
            "startTime": startTime,
            "duration": duration,
            "locationLat": locationLat,
            "locationLong": locationLong,
            "radius": radius,
            "description": description,
            "emails": emails
        },
    )
    assert response.json["error"] == "invalid token"



