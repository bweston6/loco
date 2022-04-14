#!/bin/bash
source $(pipenv --venv)/bin/activate
# building documentation
make -C docs html latexpdf
# todo - remove envvars from here
export SECRET_KEY="***REMOVED***"
export EMAIL="***REMOVED***"
export KEY="***REMOVED***"
cd src
hupper -m waitress --port=55580 Server:app
