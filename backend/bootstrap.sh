#!/bin/sh
source $(pipenv --venv)/bin/activate
hupper -m waitress --port=55580 --call loco:create_app
