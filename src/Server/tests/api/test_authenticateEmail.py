import Server.api


def test_authenticateEmail(client):
    testEmail = "test@bweston.uk"
    response = client.post("/api/authenticateEmail", json={"email": testEmail})
    assert response.json["success"] == True
