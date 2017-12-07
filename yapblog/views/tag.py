__all__ = ["tag_tag_name"]

from flask import render_template
from yapblog import app, config
from yapblog.lib.page import NavBar, SideBar
from yapblog.models import Tag

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=True, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)

sidebar = SideBar(items=[
    SideBar.TagList(
        id="tags",
        title="Tags",
        items=[
            SideBar.CollapsibleList.Item(link="/tags/CS", text="CS"),
            SideBar.CollapsibleList.Item(link="/tags/EE", text="EE"),
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


@app.route("/tags/<string:tag_name>", methods=["GET"])
def tag_tag_name(tag_name):
    tag = Tag.query.filter_by(name_ = tag_name).first()
    if tag is None:
        pass #TODO： implict bug
    return render_template(
        "tag_name_article_lists.html",
        tag_id=tag.id_,
        title=tag_name,
        navbar=navbar,
        sidebar=sidebar
    )