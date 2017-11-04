__all__ = ["api_login"]

from flask import request
from flask_login import current_user, login_user
from yapb import app
from yapb.lib.api import ok, not_ok
from yapb.models import User


@app.route("/api/login", methods=["POST"])
def api_login():
    """
    Login a user.
    Method: POST
    Parameters: name, passwd
    :return:
    Error:
        {
            "ok": False,
            "msg": "no name"|"no password"|"invalid name or password"|"already logged in"
        }
    Success:
        {
            "ok": True,
            "msg": null
        }
    """
    if current_user.is_anonymous:
        # Have not logged in
        # Get name
        try:
            name = request.form["name"]
        except KeyError:
            return not_ok("no name")
        # Get password
        try:
            passwd = request.form["passwd"]
        except KeyError:
            return not_ok("no password")
        # Query user from database
        user = User.get_user(name=name, passwd=passwd)
        if user is None:
            # Invalid
            return not_ok("invalid name or password")
        else:
            # Success
            login_user(user)
            return ok()
    else:
        # Have already logged in
        return not_ok("already logged in")
