from freezegun import freeze_time

@freeze_time("2000-09-06")
def test_getEvent(host, events, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": host["token"],
            "eventID": events["eventID"],
        }
    )
    assert response.json[""] == events["eventName"]
    assert response.json[""] == events["startTime"]
    assert response.json[""] == events["duration"]
    assert response.json[""] == events["locationLat"]
    assert response.json[""] == events["locationLong"]
    assert response.json[""] == events["radius"]
    assert response.json[""] == events["description"]
    assert response.json[""] == host["email"]
   
def test_getEvent_missingParameters(client):
    response = client.post(
        "/api/getEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_createEvent_invalidToken(host, events, client):
    response = client.post(
        "/api/getEvent",
        json={
            "token": "test",
            "eventID": events["eventID"],
        },
    )
    assert response.json["error"] == "invalid token"