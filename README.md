# Loco
This is the repository for Loco - the location based attendance app.


## API Endpoint Plan
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

## Back-End
To run the server locally:

1. Install `pipenv`.
1. Install the dependencies using `pipenv`:
	
	```
	$ cd backend
	$ pipenv install
	```
1. Run the server using the `bootstrap.sh` script:
	
	```
	$ bootstrap.sh
	```
	
	You can access the server from port 5000; it hosts from 0.0.0.0 so you can access it from all devices on your local network.