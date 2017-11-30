from flask import render_template
from flask_login import login_required, current_user
from yapblog import app
from yapblog.lib.page import NavBar
import yapblog.config as config

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)


@app.route("/login", methods=["GET"])
def login():
    return render_template("user/login.html",
                           navbar=navbar)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    return render_template("user/logout.html",
                           current_user=current_user,
                           navbar=navbar)


@app.route("/register", methods=["GET"])
def register():
    return render_template("user/register.html",
                           navbar=navbar)
