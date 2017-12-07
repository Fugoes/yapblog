__all__ = ["index"]

from flask import render_template, Markup, redirect, url_for
from yapblog import app, config
from yapblog.models import Article, Tag
from yapblog.lib.page import NavBar, SideBar

navbar = NavBar(
    title=config.WEBSITE_NAME,
    items=[
        NavBar.Item(is_active=True, link="/", text="Home"),
        NavBar.Item(is_active=False, link="/about", text="About")
    ]
)


def gen_sidebar():
    return SideBar(items=[
        SideBar.gen_tag_list()
    ])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title=config.WEBSITE_NAME,
        navbar=navbar,
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
                                   navbar=navbar,
                                   sidebar=gen_sidebar())


@app.route("/tags/<string:tag_name>", methods=["GET"])
def tags_tag_name(tag_name):
    tag = Tag.query.filter_by(name_=tag_name).first()
    if tag is None:
        return redirect(url_for("/"), code=404)
    return render_template(
        "tag.html",
        tag_id=tag.id_,
        title=tag_name,
        navbar=navbar,
        sidebar=gen_sidebar()
    )
