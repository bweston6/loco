# Loco

![Server tests badge](https://github.com/bweston6/group69_comp208/actions/workflows/server_tests.yml/badge.svg)

This is the repository for Loco - the location based attendance app.


## API Endpoint Plan
The API interface will look something like the following (these have now been implemented as stubs under [https://loco.bweston.uk/api/...](https://loco.bweston.uk/api/getUser)):

* `bool authenticateEmail(email)`
	* Sends an OTP to the email and remembers it to validate against `createUser`.
* `token|expired OTP createUser(fullName, email, hostFlag, OTP)`
	* One time password from `authenticateEmail` is passed to this endpoint.
* `user getUser(token, email)`
* `bool createEvent(token, eventID, eventName, startTimeInUnixMillis, durationInUnixMillis, locationLat, locationLong, radiusInMeters, description, email[])`
  *  If `eventID` already exists then we change the value. If not all fields must be present.
* `event getEvent(token, eventID)`
* `bool createGroup(token, groupID, groupName, email[])`
  *  If `groupID` already exists then we change the value. If not all fields must be present.
* `email[] getUsersFromGroup(token, groupID)`
* `bool setAttendance(token, email, eventID, attended)`
* `bool getAttendance(token, email, eventID)`

## Installing Dependencies
To install all project dependancies:

1. Install `pipenv` (this requires python 3).
1. Install the dependencies using `pipenv`:
	
	```
	# you should be in the same folder as the `Pipfile`
	$ pipenv install
	```

## Running the Server Locally
To run the server you should have completed [Installing Dependencies](#installing-dependencies):

1. Run the server using the `bootstrap.sh` script:
	
	```
	$ bootstrap.sh
	```
	
You can access the server from port 55580; it hosts from 0.0.0.0 so you can access it from all devices on your local network. If you want to connect to a local instance on your own computer you can use the address `127.0.0.1:55580`.

## Compiling Documentation
To compile the documentation you should have completed [Installing Dependencies](#installing-dependencies):

1. Enter the environment created by `pipenv`:

	```
	$ pipenv shell
	```
1. Enter the `docs` folder:

	```
	$ cd docs
	```
1. Build the documentation (you need to have `make` installed to do this):

	```
	$ make [target]
	```
	
	Available targets include:
	
	* `html` - Build as a website under `_build/html`.
	* `latexpdf` - Builds as a pdf under `_build/latex` (you need to have a *full* install of `texlive` to complete this target).
