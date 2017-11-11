__all__ = ["login"]

from flask import render_template
from yapblog import app


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")
