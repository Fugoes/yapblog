__all__ = ["api_user"]

from flask import request
from yapb import app, db
from yapb.models import User
from yapb.lib.api import ok, not_ok


@app.route("/api/user", methods=["GET", "POST"])
def api_user():
    if request.method == "GET":
        name, email, passwd = map(request.args.get, ["name", "email", "passwd"])
        if name is None and email is None and passwd is None:
            return ok([user.to_dict() for user in User.query.all()])
        if name is not None and email is None and passwd is not None:
            user = User.get_user(name=name, passwd=passwd)
            if user is None:
                return not_ok()
            else:
                return ok(user.to_dict())
        if name is None and email is not None and passwd is None:
            user = User.get_user(email=email, passwd=passwd)
            if user is None:
                return not_ok()
            else:
                return ok(user.to_dict())
    elif request.method == "POST":
        try:
            new_user = User(name=request.form["name"], email=request.form["email"], passwd=request.form["passwd"])
        except KeyError:
            return not_ok()
        db.session.add(new_user)
        db.session.commit()
        return ok()
    else:
        return not_ok()
