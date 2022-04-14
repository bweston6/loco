#!/bin/bash
source $(pipenv --venv)/bin/activate
# building documentation
make -C docs html latexpdf
# todo - remove envvars from here
export SECRET_KEY="b'\xe8\xc6\xd3Oa]=R#\xe7O\xb0\xd2\xdc\xa4g\x835I\xbbS\xf1\n\xd1'"
export EMAIL="b.weston60@gmail.com"
export KEY="pwarsbtwojkaiuci"
cd src
hupper -m waitress --port=55580 Server:app
