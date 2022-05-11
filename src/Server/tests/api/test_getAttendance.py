def test_getAttendance(attendee, host, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": events["eventID"],
        },
    )
    assert response.json["attendance"] == attendances["attendance_flag"]
    
def test_getAttendance_missingParameters(attendee, host, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_getAttendance_invalidToken(attendee, host, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": "test",
            "email": attendee["email"],
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid token"

def test_getAttendance_invalidEventID(attendee, host, events, attendances, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": 0000000000000,
        },
    )
    assert response.json["error"] == "invalid event ID"
