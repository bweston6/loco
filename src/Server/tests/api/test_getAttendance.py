def test_getAttendance(host, attendee, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": host["token"],
            "email": attendee["email"],
            "eventID": events["eventID"],
        },
    )
    print(response.json)
    print(response.json["attendanceFlag"])
    print(attendances["attendanceFlag"])
    assert response.json["attendanceFlag"] == attendances["attendanceFlag"]


def test_getAttendance_missingParameters(client):
    response = client.post(
        "/api/getAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"


def test_getAttendance_invalidToken(host, attendee, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": "test",
            "email": attendee["email"],
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid token"


def test_getAttendance_invalidEventID(host, attendee, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": host["token"],
            "email": attendee["email"],
            "eventID": 0000000000000,
        },
    )
    assert response.json["error"] == "invalid email or eventID"


def test_getAttendance_invalidEmail(host, attendee, events, attendances, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": host["token"],
            "email": "test@bweston.uk",
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid email or eventID"
