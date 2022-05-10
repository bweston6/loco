import json

def test_createGroup_withoutID(host, groupName, emails, conn, client):
    response = client.post(
        "/api/createGroup",
        json={
            "token": host["token"],
            "groupName": groupName,
            "emails": emails
        },
    )
    groupID = (
        "SELECT LAST_INSERT_ID()"
    )
    group = (
        "SELECT * "
        "FROM `groups` "
        "WHERE group_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(groupID)
    groupID = cursor.fetchone()[0]
    cursor.execute(group, (groupID+1,))
    group = cursor.fetchone()
    assert group[0] == groupID+1
    assert group[1] == groupName
    assert group[2] == host["email"]
    assert json.loads(group[3].decode("UTF-8")) == emails

def test_createGroup_withID(host, group, otherGroupName, otherEmails, conn, client):
    response = client.post(
        "/api/createGroup",
        json={
            "groupID": group["groupID"],
            "token": host["token"],
            "groupName": otherGroupName,
            "emails": otherEmails
        },
    )
    groupGet = (
        "SELECT * "
        "FROM `groups` "
        "WHERE group_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(groupGet, (group["groupID"], ))
    groupGet = cursor.fetchone()
    assert groupGet[0] == group["groupID"]
    assert groupGet[1] == otherGroupName
    assert groupGet[2] == group["hostEmail"]
    assert json.loads(groupGet[3].decode("UTF-8")) == otherEmails

def test_createGroup_missingParameters(client):
    response = client.post(
        "/api/createGroup",
        json={},
    )
    assert response.json["error"] == "missing parameters"

def test_createGroup_invalidToken(host, groupName, emails, client):
    response = client.post(
        "/api/createGroup",
        json={
            "token": "",
            "groupName": groupName,
            "emails": emails
        },
    )
    print(response.json)
    assert response.json["error"] == "invalid token"

# def test_createGroup_databaseError(host, conn, client):
#     response = client.post(
#         "/api/createGroup",
#         json={
#             "token": host["token"],
#             "groupName": None,
#             "emails": None
#         },
#     )
#     assert response.json["error"] == "database error"