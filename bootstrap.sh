#!/bin/bash
source $(pipenv --venv)/bin/activate

# building documentation
make -C docs html latexpdf

# Set the environment variables here, or in an rc file local to the user (see README.md):
#export SECRET_KEY=""
#export EMAIL=""
#export KEY=""

cd src
hupper -m waitress --port=55580 Server:app
