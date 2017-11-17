__all__ = ["login"]

from flask import render_template
from yapblog import app
from yapblog.lib.header import Header


@app.route("/login", methods=["GET"])
def login():
    header = Header(title="Login", name="Hi", items=[
        {"name": "Hello"}, {"name": "World"}
    ])
    return render_template("login.html", header=header)
