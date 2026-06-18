from flask import request

def reset():

    email = request.args.get("email")

    return f"Password reset sent to {email}"
