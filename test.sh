#!/bin/bash
source $(pipenv --venv)/bin/activate

# Set the environment variables here, or in an rc file local to the user (see README.md):
#export SECRET_KEY=""
#export EMAIL=""
#export KEY=""

cd src
pytest $@ Server
