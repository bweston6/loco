#!/bin/sh
source $(pipenv --venv)/bin/activate
export SECRET_KEY="b'\xe8\xc6\xd3Oa]=R#\xe7O\xb0\xd2\xdc\xa4g\x835I\xbbS\xf1\n\xd1'"
hupper -m waitress --port=55580 --call loco:create_app
