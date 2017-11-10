__all__ = ["logout"]

from flask import render_template
from flask_login import login_required
from yapblog import app


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    return render_template("logout.html")
