__all__ = ["api_logout"]

from flask_login import current_user, logout_user
from yapb import app
from yapb.lib.api import ok, not_ok


@app.route("/api/logout", methods=["GET"])
def api_logout():
    """
    Logout current user.
    Method: GET
    :return:
    Error:
        {
            "ok": False,
            "msg": "not logged in"
        }
    Success:
        {
            "ok": True,
            "msg": null
        }
    """
    if current_user.is_anonymous:
        # No user for current session
        return not_ok("not logged in")
    else:
        # Logout current user
        logout_user()
        return ok()
