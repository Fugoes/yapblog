from flask import render_template
from flask_login import login_required, current_user
from yapb import app


@app.route("/user")
@login_required
def user():
    return render_template("user.html", user=current_user)
