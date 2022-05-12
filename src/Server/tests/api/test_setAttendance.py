def test_setAttendance(host, attendeeEmail, events, client, conn):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": host["token"],
            "email": attendeeEmail,
            "eventID": events["eventID"],
            "attendanceFlag": True
        },
    )
    cursor = conn.cursor()
    attendance = """SELECT *
                FROM attendance
                WHERE email=? AND event_ID=?
    """
    cursor.execute(attendance, (attendeeEmail, events["eventID"]))
    assert attendance[0] == attendeeEmail
    assert attendance[1] == events["eventID"]
    assert attendance[2] == True


def test_setAttendance_missingParameters(client):
    response = client.post(
        "/api/setAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"


def test_setAttendance_invalidToken(host, attendeeEmail, events, attendance, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": "test",
            "email": attendeeEmail,
            "eventID": events["eventID"],
            "attended": True
        },
    )
    assert response.json["error"] == "invalid token"

def test_setAttendance_invalidEventID(host, attendeeEmail, events, attendance, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": host["token"],
            "email": attendeeEmail,
            "eventID": 0000000000000,
            "attended": True
        },
    )
    assert response.json["error"] == "invalid eventID"

