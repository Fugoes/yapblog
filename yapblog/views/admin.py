__all__ = ["admin", "admin_article_add", "admin_article"]

from flask import render_template
from yapblog import app
from yapblog.models import User, Article, Comment
from yapblog.lib.page import SideBar, get_navbar
from yapblog.lib.auth import admin_required

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
            SideBar.CollapsibleList.Item(link="/admin/article/search", text="Search Articles"),
            SideBar.CollapsibleList.Item(link="/admin/article/add", text="Add New Article"),
        ],
    ),
    SideBar.CollapsibleList(
        id="comment-management",
        title="Comment Management",
        items=[
            SideBar.CollapsibleList.Item(link="/admin/comment", text="View All Comments"),
            SideBar.CollapsibleList.Item(link="/admin/comment/search", text="Search Comments"),
        ],
    )
])


@app.route("/admin", methods=["GET"])
@admin_required
def admin():
    info = dict()
    info["user_count"] = User.query.count()
    info["article_count"] = Article.query.count()
    info["comment_count"] = Comment.query.count()
    return render_template("admin/index.html",
                           info=info,
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/article/add", methods=["GET"])
@admin_required
def admin_article_add():
    return render_template("admin/article_add.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/article", methods=["GET"])
@admin_required
def admin_article():
    return render_template("admin/article.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/article/search", methods=["GET"])
@admin_required
def admin_article_search():
    return render_template("admin/article_search.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/article/<int:article_id>", methods=["GET"])
@admin_required
def admin_article_article_id(article_id):
    return render_template("admin/article_id.html",
                           article_id=article_id,
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/user", methods=["GET"])
@admin_required
def admin_user():
    return render_template("admin/user.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/user/add", methods=["GET"])
@admin_required
def admin_user_add():
    return render_template("admin/user_add.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/comment", methods=["GET"])
@admin_required
def admin_comment():
    return render_template("admin/comment.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)


@app.route("/admin/comment/search", methods=["GET"])
@admin_required
def admin_comment_search():
    return render_template("admin/comment_search.html",
                           navbar=get_navbar("Admin"),
                           sidebar=sidebar)
