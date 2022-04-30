import Server.api


def test_authenticateEmail(client):
    response = client.post("/api/authenticateEmail", json={"email": "drop@bweston.uk"})
    assert response.json["success"] == True
