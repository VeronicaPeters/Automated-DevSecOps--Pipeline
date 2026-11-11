from flask import request, jsonify

def search():

    username = request.args.get("username", "")

    query = "SELECT * FROM users WHERE username = ?"

    return jsonify({
        "query": query,
        "parameter": username,
        "message": "Parameterized query prepared"
    })
