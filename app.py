from flask import Flask

app = Flask(__name__)

from routes.auth import login
from routes.admin import users
from routes.search import search
from routes.reset import reset

app.add_url_rule('/login', 'login', login)
app.add_url_rule('/admin/users', 'users', users)
app.add_url_rule('/search', 'search', search)
app.add_url_rule('/reset-password', 'reset', reset)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
