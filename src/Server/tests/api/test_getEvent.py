from freezegun import freeze_time

@freeze_time("2000-09-06")
def test_getEvent(host, events, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": host["token"],
            "eventId": events["eventID"],
        }
    )
    assert response.json["eventId"] == events["eventID"]
    assert response.json["eventName"] == events["eventName"]
    assert response.json["startTime"] == events["startTime"]
    assert response.json["duration"] == events["duration"]
    assert response.json["locationLat"] == events["locationLat"]
    assert response.json["locationLong"] == events["locationLong"]
    assert response.json["radius"] == events["radius"]
    assert response.json["description"] == events["description"]
    assert response.json["email"] == events["hostEmail"]
   
def test_getEvent_missingParameters(client):
    response = client.post(
        "/api/getEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_getEvent_invalidToken(host, events, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": "test",
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid token"

def test_getEvent_invalidEventID(host, events, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": host["token"],
            "eventID": 0000000000000,
        },
    )
    assert response.json["error"] == "invalid event ID"