from flask import render_template
from flask_login import login_required, current_user
from yapblog import app
from yapblog.lib.page import get_navbar


@app.route("/login", methods=["GET"])
def login():
    return render_template("user/login.html",
                           navbar=get_navbar("Login"))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    return render_template("user/logout.html",
                           current_user=current_user,
                           navbar=get_navbar("Logout"))


@app.route("/register", methods=["GET"])
def register():
    return render_template("user/register.html",
                           navbar=get_navbar("Register"))
