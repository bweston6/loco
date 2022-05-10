from freezegun import freeze_time

@freeze_time("2000-09-06")

def test_createEvent_withoutID(hostToken, eventName, startTime, duration, locationLong, locationLat, radius, description, emails, hostEmail, conn, client):
    response = client.post(
        "/api/createEvent",
        json={
            "token": hostToken,
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
        "SELECT LAST_INSERT_ID()"
    )
    event = (
        "SELECT * "
        "FROM events "
        "WHERE event_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(eventID)
    eventID = cursor.fetchone()
    cursor.execute(event, eventID)
    event = cursor.fetchone()
    conn.commit()
    assert event[0] == eventID
    assert event[1] == eventName
    assert event[2] == startTime
    assert event[3] == duration
    assert event[4] == locationLat
    assert event[5] == locationLong
    assert event[6] == radius
    assert event[7] == description
    assert event[8] == hostEmail

def test_createEvent_withID(events, hostToken, otherEventName, otherStartTime, otherDuration, otherLocationLat, otherLocationLong, otherRadius, otherDescription, otherEmails, conn, client):
    response = client.post(
        "/api/createEvent",
        json={
            "eventID": events["eventID"],
            "token": hostToken,
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
        "SELECT * "
        "FROM events "
        "WHERE event_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(event, events["eventID"])
    event = cursor.fetchone()
    conn.commit()
    assert event[0] == events["eventID"]
    assert event[1] == otherEventName
    assert event[2] == otherStartTime
    assert event[3] == otherDuration
    assert event[4] == otherLocationLat
    assert event[5] == otherLocationLong
    assert event[6] == otherRadius
    assert event[7] == otherDescription
    assert event[8] == events["hostEmail"]

def test_createEvent_missingParameters(client):
    response = client.post(
        "/api/createEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_createEvent_invalidToken(host, client):
    response = client.post(
        "/api/createEvent",
        json={
            "token": "idk",
            "eventName": otherEventName,
            "startTime": otherStartTime,
            "duration": otherDuration,
            "locationLat": otherLocationLat,
            "locationLong": otherLocationLong,
            "radius": otherRadius,
            "description": otherDescription,
            "emails": otherEmails
        },
    )
    assert response.json["error"] == "invalid token"



