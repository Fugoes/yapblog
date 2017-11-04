__all__ = ["api_logout"]

from flask_login import current_user, logout_user
from yapb import app
from yapb.lib.api import ok, not_ok


@app.route("/api/logout", methods=["GET"])
def api_logout():
    if current_user.is_anonymous:
        return not_ok("not logged in")
    else:
        logout_user()
        return ok("success")
