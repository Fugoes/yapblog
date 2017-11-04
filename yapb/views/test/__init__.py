from flask import render_template
from yapb import app
from yapb.models import User


@app.route("/test/show_users")
def test_show_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/test/show_users_with_api")
def test_show_users_with_api():
    return render_template("users_api.html")
