def test_getAttendee(attendee, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": attendee["token"],
            "email": attendee["email"],
        },
    )
    assert response.json["fullName"] == attendee["name"]
    assert response.json["email"] == attendee["email"]
    assert response.json["hostFlag"] == attendee["hostFlag"]
    assert "eventIDs" in response.json
    assert not "groupIDs" in response.json
    assert not "error" in response.json


def test_getAttendee_fromHost(host, attendee, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": host["token"],
            "email": attendee["email"],
        },
    )
    assert response.json["fullName"] == attendee["name"]
    assert response.json["email"] == attendee["email"]
    assert response.json["hostFlag"] == attendee["hostFlag"]
    assert "eventIDs" in response.json
    assert not "groupIDs" in response.json
    assert not "error" in response.json


def test_getAttendee_fromOtherAttendee(attendee, otherAttendee, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": otherAttendee["token"],
            "email": attendee["email"],
        },
    )
    assert response.json["fullName"] == attendee["name"]
    assert response.json["email"] == attendee["email"]
    assert response.json["hostFlag"] == attendee["hostFlag"]
    assert not "eventIDs" in response.json
    assert not "groupIDs" in response.json
    assert not "error" in response.json


def test_getHost(host, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": host["token"],
            "email": host["email"],
        },
    )
    assert response.json["fullName"] == host["name"]
    assert response.json["email"] == host["email"]
    assert response.json["hostFlag"] == host["hostFlag"]
    assert "eventIDs" in response.json
    assert "groupIDs" in response.json
    assert not "error" in response.json


def test_getHost_fromAttendee(attendee, host, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": attendee["token"],
            "email": host["email"],
        },
    )
    assert response.json["fullName"] == host["name"]
    assert response.json["email"] == host["email"]
    assert response.json["hostFlag"] == host["hostFlag"]
    assert not "eventIDs" in response.json
    assert not "groupIDs" in response.json
    assert not "error" in response.json


def test_getHost_fromOtherHost(host, otherHost, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": otherHost["token"],
            "email": host["email"],
        },
    )
    assert response.json["fullName"] == host["name"]
    assert response.json["email"] == host["email"]
    assert response.json["hostFlag"] == host["hostFlag"]
    assert not "eventIDs" in response.json
    assert not "groupIDs" in response.json
    assert not "error" in response.json


def test_getUser_invalidEmail(host, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": host["token"],
            "email": "test@bweston.uk",
        },
    )
    assert response.json["error"] == "email is not registered"


def test_getUser_invalidToken(host, client):
    response = client.post(
        "/api/getUser",
        json={
            "token": "",
            "email": host["email"],
        },
    )
    assert response.json["error"] == "invalid token"
    assert True


def test_getUser_missingParameters(client):
    response = client.post(
        "/api/getUser",
        json={},
    )
    assert response.json["error"] == "missing parameters"
