__all__ = ["register"]

from flask import request, render_template
from yapblog import app


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")
