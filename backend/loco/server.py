#!/usr/bin/env python

from os import system
from flask import Flask, jsonify, request

api = Flask(__name__)

baseurl = "/api"
users = []

@api.route(baseurl + "/users")
def getUsers():
	#Returns the users.
	
    #Returns:
    #  users: a list of registers users.
	
    return jsonify(users)

@api.route(baseurl + "/users", methods=["POST"])
def addUser():
    users.append(request.get_json())
    return "", 204

@api.route(baseurl + "/webhook", methods=["POST"])
def webook():
    system("export GIT_SSH_COMMAND='ssh -i /home/loco/.ssh/loco-backend -o IdentitiesOnly=yes'; git fetch; git reset origin/base --hard; git pull")
    return "ok"
