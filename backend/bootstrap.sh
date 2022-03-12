#!/bin/sh
source $(pipenv --venv)/bin/activate
cd loco
hupper -m waitress --port=55580 server:api
