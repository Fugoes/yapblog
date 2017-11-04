from flask import request, render_template, redirect, g
from flask_login import login_user
from yapb import app
from yapb.models import User


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        user = User.get_user(name=request.form["name"], passwd=request.form["passwd"])
        if user is None:
            return render_template("login.html")
        else:
            login_user(user)
            return redirect("/user")
