#!/bin/bash
source $(pipenv --venv)/bin/activate
# todo - remove envvars from here
export SECRET_KEY="***REMOVED***"
export EMAIL="***REMOVED***"
export KEY="***REMOVED***"
cd src
hupper -m waitress --port=55580 Server:create_app
