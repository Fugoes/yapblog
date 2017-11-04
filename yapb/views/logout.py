from flask_login import logout_user, login_required
from yapb import app


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return "Logout"
