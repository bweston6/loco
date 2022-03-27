#!/bin/sh
source $(pipenv --venv)/bin/activate
export SECRET_KEY="***REMOVED***"
hupper -m waitress --port=55580 --call loco:create_app
