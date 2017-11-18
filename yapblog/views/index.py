__all__ = ["index"]

from flask import render_template
from yapblog import app, config
from yapblog.lib.page import NavBar, SideBar


@app.route("/", methods=["GET"])
def index():
    navbar = NavBar(
        title=config.WEBSITE_NAME,
        items=[
            NavBar.Item(is_active=True, link="/", text="Home"),
            NavBar.Item(is_active=False, link="/about", text="About")
        ]
    )
    sidebar = SideBar(items=[
        SideBar.CollapsibleList(
            id="user-management",
            title="User Management",
            items=[
                SideBar.CollapsibleList.Item(link="/", text="First"),
                SideBar.CollapsibleList.Item(link="/", text="Second"),
            ],
        ),
        SideBar.CollapsibleList(
            id="article-management",
            title="Article Management",
            items=[
                SideBar.CollapsibleList.Item(link="/", text="First"),
                SideBar.CollapsibleList.Item(link="/", text="Second"),
            ],
        ),
    ])
    return render_template(
        "index.html",
        title=config.WEBSITE_NAME,
        navbar=navbar,
        sidebar=sidebar
    )
