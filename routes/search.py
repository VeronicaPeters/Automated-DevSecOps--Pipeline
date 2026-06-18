from flask import request

def search():

    username = request.args.get("username")

    query = f"""
    SELECT *
    FROM users
    WHERE username='{username}'
    """

    return query
