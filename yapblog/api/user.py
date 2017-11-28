__all__ = ["api_user", "api_user_register", "api_user_login", "api_user_logout"]

from flask import request
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from yapblog import app, db
from yapblog.models import User
from yapblog.lib.api import ok, not_ok
from yapblog.lib.auth import md5_with_salt


@app.route("/api/user/me", methods=["GET"])
def api_user_me():
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
        "id": <this user's id>,
        "name": <this user's name>,
        "email": <this user's email>
    }
    """
    if current_user.is_anonymous:
        return not_ok()
    else:
        return ok(uid=current_user.id_,
                  name=current_user.name_,
                  email=current_user.email_)


@app.route("/api/user/new", methods=["POST"])
def api_user_new():
    """
    Create a new user. For admin only.

    Method: POST

    Parameter: name, email, passwd, is_admin

    :return:
    If the parameters is not valid:
    {
        "ok": False,
    }
    If success:
    {
        "ok": True,
        "id": <user's id>
    }
    """
    data = request.get_json()
    try:
        name = data["name"]
        email = data["email"]
        passwd = data["passwd"]
        is_admin = data["is_admin"]
    except KeyError:
        return not_ok()
    new_user = User(name, email, md5_with_salt(passwd), is_admin)
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        return not_ok()
    return ok(id=new_user.id_)


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
        }
        If success:
        {
            "ok": True,
            "id": <user's id>
        }
    """
    if not current_user.is_anonymous:
        return not_ok(msg="not anonymous")
    else:
        data = request.get_json()
        try:
            name = data["name"]
            email = data["email"]
            passwd = data["passwd"]
        except KeyError:
            return not_ok()
        new_user = User(name, email, md5_with_salt(passwd))
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            return not_ok()
        return ok(id=new_user.id_)


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
    data = request.get_json()
    if not current_user.is_anonymous:
        return not_ok(msg="already logged in")
    else:
        user = User.query.filter_by(name_=data["name"],
                                    passwd_hash_=md5_with_salt(data["passwd"]))
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


@app.route("/api/user", methods=["GET"])
def api_user():
    """
    Get all users info.

    Method: GET

    :return:
    If success:
    {
        "ok": True
        "users:
        [{
            "id": <user.id>,
            "name": <user.name>,
            "email": <user.email>
        }]
    }
    Else:
    {
        "ok": False
    }
    """
    users = User.query.all()
    return ok(users=[{
        "id": user.id_,
        "name": user.name_,
        "email": user.email_
    } for user in users])


@app.route("/api/user/<int:user_id>", methods=["GET"])
def api_user_user_id_get(user_id):
    """
    Get user with id of user_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "id": <user.id>,
        "name": <user.name>,
        "email": <user.email>,
        "passwd_hash": <user.passwd_hash>
    }
    """
    user = User.query.filter_by(id_=user_id).first()
    if user is None:
        return not_ok()
    return ok(id=user.id_,
              name=user.name_,
              email=user.email_,
              passwd_hash=user.passwd_hash_)


@app.route("/api/user/<int:user_id>", methods=["DELETE"])
def api_user_user_id_delete(user_id):
    """
    Delete the user with id of user_id.

    Method: DELETE

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True
    }
    """
    User.query.filter_by(id_=user_id).delete()
    db.session.commit()
    return ok()
