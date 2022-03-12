from flask import Flask, jsonify, request

app = Flask(__name__)

users = []

@app.route("/users")
def getUsers():
    return jsonify(users)

@app.route("/users", methods=["POST"])
def addUser():
    users.append(request.get_json())
    return "", 204
