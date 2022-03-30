#!/bin/sh
source $(pipenv --venv)/bin/activate
# todo - remove envvars from here
export SECRET_KEY="***REMOVED***"
export EMAIL="***REMOVED***"
export KEY="***REMOVED***"
hupper -m waitress --port=55580 --call loco:create_app "$@"
