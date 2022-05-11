def test_getAttendance(host,attendee,events,client,attaendance):
    response = client.post(
        "/api/getAttendance",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
            "eventID": events["eventID"]
        },
    )
    assert attendance["attendance_flag"] == True
    
    
def test_getAttendance_missingParameters(client):
    response = client.post(
        "/api/setAttendance",
        json={},
    )
    assert response.json["error"] == "missing parameters"

    
def test_getAttendance_databaseError(host,client):
    response = client.post(
        "/api/setAttendance",
    )
    assert response.json["error"] == "database error"
