# Loco
This is the repository for Loco - the location based attendance app.


## API Endpoint Plan
The API interface will look something like the following (these have now been implemented as stubs under [https://loco.bweston.uk/api/...](https://loco.bweston.uk/api/getUser)):

* `token createUser(fullName, email, hostFlag)`
* `user getUser(token, email)`
* `bool createEvent(token, eventID, eventName, startTimeInUnixMillis, durationInUnixMillis, locationLat, locationLong, radiusInMeters, description, email[])`
  *  If `eventID` already exists then we change the value. If not all fields must be present.
* `event getEvent(token, eventID)`
* `bool createGroup(token, groupID, groupName, email[])`
  *  If `groupID` already exists then we change the value. If not all fields must be present.
* `email[] getUsersFromGroup(token, groupID)`
* `bool setAttendance(token, email, eventID, attended)`
* `bool getAttendance(token, email, eventID)`

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
	
	You can access the server from port 55580; it hosts from 0.0.0.0 so you can access it from all devices on your local network. If you want to connect to a local instance on your own computer you can use the address `127.0.0.1:55580`.
