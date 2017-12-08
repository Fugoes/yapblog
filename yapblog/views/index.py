__all__ = ["index"]

from flask import render_template, Markup, redirect, url_for
from flask_login import current_user
from yapblog import app, config
from yapblog.models import Article, Tag
from yapblog.lib.page import NavBar, SideBar, get_navbar


def gen_sidebar():
    return SideBar(items=[
        SideBar.gen_tag_list()
    ])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title=config.WEBSITE_NAME,
        navbar=get_navbar("Home"),
        sidebar=gen_sidebar()
    )


@app.route("/<int:year>/<int:month>/<string:title>", methods=["GET"])
def article_year_month_title(year, month, title):
    article = Article.query.filter_by(title_=title).first()
    if article is not None:
        date = article.date_time_
        if date.year == year and date.month == month:
            return render_template("article.html",
                                   title=title,
                                   html_content=Markup(article.html_content_),
                                   navbar=get_navbar(None),
                                   sidebar=gen_sidebar())
    else:
        return redirect("/", code=404)


@app.route("/tags/<string:tag_name>", methods=["GET"])
def tags_tag_name(tag_name):
    tag = Tag.query.filter_by(name_=tag_name).first()
    if tag is None:
        return redirect("/", code=404)
    return render_template(
        "tag.html",
        tag_id=tag.id_,
        title=tag_name,
        navbar=get_navbar(None),
        sidebar=gen_sidebar()
    )
