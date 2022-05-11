def test_getUsersFromGroup(host, group, client):
    response = client.post(
        "/api/getUsersFromGroup",
        json={
            "token": host["token"],
            "groupID": group["groupID"],
        },
    )
    assert response.json["emails"] == group["emails"]


def test_getUsersFromGroup_missingParameters(client):
    response = client.post(
        "/api/getUsersFromGroup",
        json={},
    )
    assert response.json["error"] == "missing parameters"


def test_getUsersFromGroup_invalidToken(host, group, client):
    response = client.post(
        "/api/getUsersFromGroup",
        json={"token": "", "groupID": group["groupID"]},
    )
    assert response.json["error"] == "invalid token"
