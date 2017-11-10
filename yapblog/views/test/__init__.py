__all__ = ["test_show_users_with_api", "test_show_users"]

from flask import render_template
from yapblog import app
from yapblog.models import User


@app.route("/test/show_users")
def test_show_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/test/show_users_with_api")
def test_show_users_with_api():
    return render_template("users_api.html")
