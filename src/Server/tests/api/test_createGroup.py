def test_createGroup_withoutID(hostToken, groupName, hostEmail, emails, conn, client):
    response = client.post(
        "/api/createGroup",
        json={
            "token": hostToken,
            "groupName": groupName,
            "emails": emails
        },
    )
    groupID = (
        "SELECT LAST_INSERT_ID()"
    )
    group = (
        "SELECT * "
        "FROM groups "
        "WHERE group_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(groupID)
    groupID = cursor.fetchone()
    cursor.execute(group, groupID)
    group = cursor.fetchone()
    conn.commit()
    assert group[0] == groupID
    assert group[1] == groupName
    assert group[2] == hostEmail
    assert group[3] == emails

def test_createGroup_withID(group, hostToken, otherGroupName, otherEmails, conn, client):
    response = client.post(
        "/api/createGroup",
        json={
            "groupID": group["groupID"],
            "token": hostToken,
            "groupName": otherGroupName,
            "emails": otherEmails
        },
    )
    group = (
        "SELECT * "
        "FROM groups "
        "WHERE group_ID = ?"
    )
    cursor = conn.cursor()
    cursor.execute(group, group["groupID"])
    group = cursor.fetchone()
    assert group[0] == group["groupID"]
    assert group[1] == otherGroupName
    assert group[2] == group["hostEmail"]
    assert group[3] == otherEmails

def test_createGroup_missingParameters(client):
    response = client.post(
        "/api/createGroup",
        json={}
    )
    assert response.json["error"] == "missing parameters"

#def test_createGroup_invalidToken():
