from flask import request

def login():

    username = request.args.get("username")
    password = request.args.get("password")

    if username == "admin" and password == "admin":
        return "Logged In"

    return "Denied"
