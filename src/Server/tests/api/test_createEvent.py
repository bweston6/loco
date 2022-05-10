from freezegun import freeze_time

@freeze_time("2000-09-06")
def test_createEvent_withoutID(hostToken, eventName, startTime, duration, locationLong, locationLat, radius, description, 
emails, hostEmail, conn, client):
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
            "emails": emails
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
    assert event[2] == hostEmail
    assert event[3] == startTime
    assert event[4] == locationLong
    assert event[5] == locationLat
    assert event[6] == radius
    assert event[7] == description
    assert event[8] == hostEmail

def test_createEvent_withID(event, hostToken, otherEventName, otherStartTime, otherDuration, otherLocationLat, 
otherLocationLong, otherRadius, otherDescription, otherEmails, conn, client):
    response = client.post(
        "/api/createEvent",
        json={
            "eventID": event["eventID"],
            "token": hostToken,
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
    event = (
        "SELECT * "
        "FROM events "
        "WHERE event_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(event, event["eventID"])
    event = cursor.fetchone()
    conn.commit()
    assert event[0] == event["eventID"]
    assert event[1] == eventName
    assert event[2] == hostEmail
    assert event[3] == startTime
    assert event[4] == locationLong
    assert event[5] == locationLat
    assert event[6] == radius
    assert event[7] == description
    assert event[8] == event["hostEmail"]


def test_createEvent_missingParameters(client):
    response = client.post(
        "/api/createEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"

