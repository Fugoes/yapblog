from flask import render_template, Markup
from yapblog import app
from yapblog.models import Article
from yapblog.lib.page import NavBar
from yapblog import config

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)


