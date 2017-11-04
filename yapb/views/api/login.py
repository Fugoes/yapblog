__all__ = ["api_login"]

from flask import request
from flask_login import current_user, login_user
from yapb import app
from yapb.lib.api import ok, not_ok
from yapb.models import User


@app.route("/api/login", methods=["POST"])
def api_login():
    if current_user.is_anonymous:
        try:
            name = request.form["name"]
        except KeyError:
            return not_ok("no name")

        try:
            passwd = request.form["passwd"]
        except KeyError:
            return not_ok("no password")

        user = User.get_user(name=name, passwd=passwd)
        if user is None:
            return not_ok("invalid name or password")
        else:
            login_user(user)
            return ok("success")
    else:
        return not_ok("already logged in")
