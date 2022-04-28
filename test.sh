#!/bin/bash
source $(pipenv --venv)/bin/activate
# todo - remove envvars from here
export SECRET_KEY="***REMOVED***"
export EMAIL="***REMOVED***"
export KEY="***REMOVED***"
cd src
pytest Server
