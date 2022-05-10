def test_getEvent_missingParameters(client):
    response = client.post(
        "/api/getEvent",
        json={},
    )
    assert response.json["error"] == "missing parameters"
