def test_setAttendance(host, attendee, events, client, conn):
    response = client.post(
        "/api/setAttendance",
        json={
            "token": host["token"],
            "email": attendee["email"],
            "eventID": events["eventID"],
            "attended": True
        },
    )
    cursor = conn.cursor()
    query = """SELECT attendance_flag
                FROM attendance
                WHERE email=? AND event_ID=?
    """
    cursor.execute(query, (attendee["email"], events["eventID"]))
    assert cursor.fetchone()[0] == True


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

## You should implement a check in setAttendance so that using invalid eventIDs doesn't
## produce a database error

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
    assert response.json["error"] == "invalid event ID"

## Using invalid emails is a valid usecase as it allows for registration before someone
## has made their account

# def test_setAttendance_invalidEmail(host, attendee, events, attendance, client):
#     response = client.post(
#         "/api/setAttendance",
#         json={
#             "token": host["token"],
#             "email": "test@bweston.uk",
#             "eventID": events["eventID"],
#             "attended": True
#         },
#     )
#     assert response.json["error"] == "email is not registered"
