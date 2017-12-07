__all__ = ["admin", "admin_article_add", "admin_article"]

from flask import render_template
from yapblog import app, config
from yapblog.models import User, Article
from yapblog.lib.page import SideBar, NavBar

sidebar = SideBar(items=[
    SideBar.CollapsibleList(
        id="user-management",
        title="User Management",
        items=[
            SideBar.CollapsibleList.Item(link="/admin/user", text="View All Users"),
            SideBar.CollapsibleList.Item(link="/admin/user/add", text="Add New User"),
        ],
    ),
    SideBar.CollapsibleList(
        id="article-management",
        title="Article Management",
        items=[
            SideBar.CollapsibleList.Item(link="/admin/article", text="View All Articles"),
            SideBar.CollapsibleList.Item(link="/admin/article/add", text="Add New Article"),
        ],
    )
])

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=False, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)


@app.route("/admin", methods=["GET"])
def admin():
    info = dict()
    info["user_count"] = User.query.count()
    info["article_count"] = Article.query.count()
    return render_template("admin/index.html",
                           info=info,
                           navbar=navbar,
                           sidebar=sidebar)


@app.route("/admin/article/add", methods=["GET"])
def admin_article_add():
    return render_template("admin/article_add.html",
                           navbar=navbar,
                           sidebar=sidebar)


@app.route("/admin/article", methods=["GET"])
def admin_article():
    return render_template("admin/article.html",
                           navbar=navbar,
                           sidebar=sidebar)


@app.route("/admin/article/<int:article_id>", methods=["GET"])
def admin_article_article_id(article_id):
    return render_template("admin/article_id.html",
                           article_id=article_id,
                           navbar=navbar,
                           sidebar=sidebar)


@app.route("/admin/user", methods=["GET"])
def admin_user():
    return render_template("admin/user.html",
                           navbar=navbar,
                           sidebar=sidebar)


@app.route("/admin/user/add", methods=["GET"])
def admin_user_add():
    return render_template("admin/user_add.html",
                           navbar=navbar,
                           sidebar=sidebar)
