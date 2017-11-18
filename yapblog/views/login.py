__all__ = ["login"]

from flask import render_template
from yapblog import app
from yapblog.lib.page import NavBar
import yapblog.config as config


@app.route("/login", methods=["GET"])
def login():
    navbar = NavBar(
        title=config.WEBSITE_NAME,
        items=[
            NavBar.Item(is_active=False, link="/", text="Home"),
            NavBar.Item(is_active=False, link="/about", text="About")
        ]
    )
    return render_template(
        "login.html",
        navbar=navbar
    )
