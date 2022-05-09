# being worked on by Ben
# todo - remove this message

from Server import auth
from freezegun import freeze_time


@freeze_time("2000-09-06")
def test_createHost(hostEmail, hostName, hostOTP, hostToken, conn, client):
    response = client.post(
        "/api/createUser",
        json={
            "OTP": hostOTP,
            "fullName": hostName,
            "email": hostEmail,
            "hostFlag": True,
        },
    )
    assert response.json["token"] == hostToken
    user = """SELECT *
        FROM users
        WHERE email = ?
    """
    cursor = conn.cursor()
    cursor.execute(user, (hostEmail,))
    user = cursor.fetchone()
    assert user[0] == hostName
    assert user[1] == hostEmail
    assert user[2] == hostToken
    assert user[3] == True


@freeze_time("2000-09-06")
def test_createAttendee(
    attendeeEmail, attendeeName, attendeeOTP, attendeeToken, conn, client
):
    response = client.post(
        "/api/createUser",
        json={
            "OTP": attendeeOTP,
            "fullName": attendeeName,
            "email": attendeeEmail,
            "hostFlag": False,
        },
    )
    assert response.json["token"] == attendeeToken
    user = """SELECT *
        FROM users
        WHERE email = ?
    """
    cursor = conn.cursor()
    cursor.execute(user, (attendeeEmail,))
    user = cursor.fetchone()
    assert user[0] == attendeeName
    assert user[1] == attendeeEmail
    assert user[2] == attendeeToken
    assert user[3] == False
