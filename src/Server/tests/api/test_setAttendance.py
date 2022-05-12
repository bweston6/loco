def test_setAttendance(host, attendee, events, client, conn):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": host["token"],
            "email": attendee["email"],
            "eventID": events["eventID"],
            "attendanceFlag": True
        },
    )
    cursor = conn.cursor()
    attendance = """SELECT *
                FROM attendance
                WHERE email=? AND event_ID=?
    """
    cursor.execute(attendance, (attendee["email"], events["eventID"]))
    assert attendance[0] == attendee["email"]
    assert attendance[1] == events["eventID"]
    assert attendance[2] == True


def test_setAttendance_missingParameters(client):
    response = client.post(
        "/api/setAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"


def test_setAttendance_invalidToken(host, attendee, events, attendance, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": "test",
            "email": attendee["email"],
            "eventID": events["eventID"],
            "attended": True
        },
    )
    assert response.json["error"] == "invalid token"

def test_setAttendance_invalidEventID(host, attendee, events, attendance, client):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": host["token"],
            "email": attendee["email"],
            "eventID": 0000000000000,
            "attended": True
        },
    )
    assert response.json["error"] == "invalid eventID"

