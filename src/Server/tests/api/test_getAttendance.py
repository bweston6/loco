def test_getAttendance(attendee, events, attendance, client):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": events["eventID"]
        },
    )
    assert response.json["attendance"] == attendance["attendance_flag"]
    
    
    
def test_getAttendance_missingParameters(client):
    response = client.post(
        "/api/getAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"

    
def test_getAttendance_databaseError(host,client):
    response = client.post(
        "/api/getAttendance",
    )
    assert response.json["error"] == "database error"
