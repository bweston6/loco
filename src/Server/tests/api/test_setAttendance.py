def test_setAttendance(host, attendee, events, client, attendance):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": events["eventID"]
        },
    )
    assert attendance["attendance_flag"] == True
    
def test_setAttendance_missingParameters(client):
    response = client.post(
        "/api/setAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_setAttendance_invalidToken(attendee, host, events, attendances, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": "test",
            "email": attendee["email"],
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid token"

def test_setAttendance_invalidEventID(attendee, host, events, attendances, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": 0000000000000,
        },
    )
    assert response.json["error"] == "invalid event ID"

def test_setAttendance_invalidEmail(attendee, host, events, attendances, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": attendee["token"],
            "email": "test@bweston.uk",
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "email is not registered"