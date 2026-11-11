from flask import request, jsonify

def reset():

    email = request.args.get("email")

    return jsonify({
        "message": "Password reset request received",
        "email": email
    })
