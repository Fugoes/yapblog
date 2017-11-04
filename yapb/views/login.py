__all__ = ["login"]

from flask import request, render_template
from yapb import app


@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
