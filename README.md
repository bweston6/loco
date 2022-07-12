# Loco

![Server lint badge](https://github.com/bweston6/group69_comp208/actions/workflows/server%20lint.yml/badge.svg)
![Server tests badge](https://github.com/bweston6/group69_comp208/actions/workflows/server%20tests.yml/badge.svg)

This is the repository for Loco - the location based attendance app. This was produced as part of a group project at the University of Liverpool. The sever is written in Python and is fully functional, the app is written for iOS and is a work in progress. Group members are:

* Oluwatimileyin (Timi) Bello
* Rostom Benhamada
* Noushin Islam
* Gunan Singh
* Leon Szabo
* Ben Weston

## Documentation
Go to [https://loco.bweston.uk/docs/](https://loco.bweston.uk/docs/) to see the documentation. This includes **user manuals** for attendees and hosts, as well as API documentation. A PDF download of this is also available at [https://loco.bweston.uk/downloads/loco.pdf](https://loco.bweston.uk/downloads/loco.pdf).

## Installing the Server
This installation guide is aimed at Debian based distros. Please refer to the package repositories for your particular distro for alternative package names (if required).

Before completing this installation, you should have an unprivileged system user that the Loco server can run under. You should download the source code to a location that this user has access to.

### Installing System Dependancies
The server requires the following programs to run:

* pipenv (`pipenv`)
* mariadb server (`mariadb-server`)
* mariadb connector (`libmariadb-dev`)
	* This may be included with the mariadb server on some distros.
* texlive (optional - for PDF documentation) (`texlive-full`)

You can install them with the following command:

```
$ sudo apt install pipenv libmariadb-dev mariadb-server texlive-full
```

### Setting Up the Database
Debian based distros will automatically enable and start the mariadb service for you. Refer to the documentation for your distro if the server is not started.

#### Securing the Database
You can secure your mariadb install by running the following command:

```
sudo mysql_secure_installation
```

---

You don't need to change the root password but you should accept the default for all other options by pressing enter.

---

#### Creating the Database and User
You can run the following to create the database and user:

```sql
$ sudo mysql
> CREATE DATABASE loco;
> CREATE USER 'username'@'localhost' IDENTIFIED VIA 'unix_socket';
> GRANT ALL PRIVILEGES ON loco.* TO 'username'@'localhost';
```

---

You should replace `username` with the username of the unprivileged user the server will run under. This is required as the server uses unix socket authentication to log into the database.

---

To exit the mariadb prompt you can enter:

```
> quit
```

### Installing Python Dependancies
Ensure you are in the root of the repository (where `Pipfile` is located) in your terminal. Enter the following to install the python dependancies in a virtual environment:

```
$ pipenv install
```

### Running the Server
You should modify the environment variables in `bootstrap.sh` with your own information:

1. `SECRET_KEY` encrypts the tokens genterated by your server. It should be different for each server and shouldn't change across the server's life.
	
	You can generate a suitable key with the following commands:
	
	```python
	$ python
	>>> import os
	>>> os.urandom(24)
	```
	
	You can exit the python prompt with:
	
	```python
	>>> exit()
	```
	
1. `EMAIL` and `KEY` are the login details for a Gmail address. You can generate an authentication key on the [app passwords](https://myaccount.google.com/apppasswords) section of your google account.

Once you have set these variables, you can run the server using this script:
	
```
$ bootstrap.sh
```
	
You can access the server from port 55580; it hosts from 0.0.0.0 so you can access it from all devices on your local network. If you want to connect to a local instance on your own computer you can use the address `127.0.0.1:55580`.

There is also a systemd service file that you should modify with the location of your source code and the name of your unprivileged user. Refer to the systemd manuals on how to install this on your system. This will allow you to start the server on boot.

## Compiling Documentation
To compile the documentation you should have completed [Installing System Dependencies](#installing-system-dependencies) and [Installing Python Dependancies](#installing-python-dependancies):

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
