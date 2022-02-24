# Loco
This is the repository for Loco - the location based attendance app.

The API interface will look something like the following:

* `bool create_user(fullName, email, hostFlag)`
* `user get_user(email)`
* `bool create_event(eventID, eventName, startTimeInUnixMillis, durationInUnixMillis, locationLat, locationLong, radiusInMeters, description, email[])`
  *  If `eventID` already exists then we change the value. If not all fields must be present.
* `event get_event(eventID)`
* `bool create_group(groupID, groupName, email[])`
  *  If `groupID` already exists then we change the value. If not all fields must be present.
* `email[] get_users_from_group(groupID)`
* `bool set_attendance(email, eventID, attended)`
* `bool get_attendance(email, eventID)`
