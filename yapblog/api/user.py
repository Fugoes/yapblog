__all__ = ["api_user", "api_user_register", "api_user_login", "api_user_logout"]

from flask import request
from flask_login import current_user, login_user, logout_user
from yapblog import app
from yapblog.models import User
from yapblog.lib.api import ok, not_ok


@app.route("/api/user", methods=["GET"])
def api_user():
    """
    Get information of this user.

    Method: GET

    :return:
    If current user is anonymous:
    {
        "ok": False
    }
    If current user is not anonymous:
    {
        "ok": True,
        "uid": <this user's id>,
        "name": <this user's name>,
        "email": <this user's email>
    }
    """
    if current_user.is_anonymous:
        return not_ok()
    else:
        return ok(uid=current_user.uid,
                  name=current_user.name,
                  email=current_user.email)


@app.route("/api/user/register", methods=["POST"])
def api_user_register():
    """
    Register a user.

    Method: POST

    Parameter: name, email, passwd

    :return:
    If current user is not anonymous:
    {
        "ok": False,
        "msg": "not anonymous"
    }
    If current user is anonymous:
        If the parameters is not valid:
        {
            "ok": False,
            "msg": "invalid parameters"
        }
        If success:
        {
            "ok": True
        }
    """
    if not current_user.is_anonymous:
        return not_ok(msg="not anonymous")
    else:
        form = request.form
        new_user = User.register_user(name=form["name"],
                                      email=form["email"],
                                      passwd=form["passwd"])
        if new_user:
            return ok()
        else:
            return not_ok(msg="invalid parameters")


@app.route("/api/user/login", methods=["POST"])
def api_user_login():
    """
    Login the user with information in parameters.

    Method: POST
    Parameter: name, passwd

    :return:
    If have already logged in:
    {
        "ok": False,
        "msg": "already logged in"
    }
    If the parameters is invalid:
    {
        "ok": False,
        "msg": "invalid"
    }
    If login successful:
    {
        "ok": True,
        "uid": <uid of the user>
    }
    """
    if not current_user.is_anonymous:
        return not_ok(msg="already logged in")
    else:
        form = request.form
        user = User.get_user(name=form.get("name"), passwd=form.get("passwd"))
        print(user)
        if user is None:
            return not_ok(msg="invalid")
        else:
            login_user(user)
            return ok(uid=user.uid)


@app.route("/api/user/logout", methods=["GET"])
def api_user_logout():
    """
    Logout current user.

    Method: GET

    :return:
    If success:
    {
        "ok": True
    }
    Else:
    {
        "ok": False
    }
    """
    if current_user.is_anonymous:
        return not_ok()
    else:
        logout_user()
        return ok()
