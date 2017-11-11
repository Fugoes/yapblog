__all__ = ["api_user"]

from flask import request
from sqlalchemy.exc import IntegrityError
from yapblog import app, db
from yapblog.models import User
from yapblog.lib.api import ok, not_ok


@app.route("/api/user", methods=["POST"])
def api_user():
    """
    Method: POST
    Parameters: name, email, passwd
    :return:
    Error:
        {
            "ok": False,
            "msg": <Error Message>
        }
    Success:
        {
            "ok": True,
            "msg": null
        }
    """
    new_user_dict = dict()
    # Get name, email and passwd
    for key in ("name", "email", "passwd"):
        try:
            new_user_dict[key] = request.form[key]
        except KeyError:
            return not_ok("no %s" % key)
    # Create new user
    new_user = User(**new_user_dict)
    try:
        # Add new user to database
        db.session.add(new_user)
        db.session.commit()
        return ok()
    except IntegrityError:
        # This user name or email is already in database
        return not_ok("invalid")
