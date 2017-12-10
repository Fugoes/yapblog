__all__ = ["index"]

from flask import render_template, Markup, redirect
from yapblog import app, config, db
from yapblog.models import Article, Tag
from yapblog.lib.page import NavBar, SideBar, get_navbar, get_archives


def gen_sidebar():
    return SideBar(items=[
        SideBar.gen_tag_list(),
        get_archives(),
    ])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "home.html",
        articles=Article.query.order_by(db.desc(Article.date_time_)).all(),
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
        articles=tag.articles,
        tag_id=tag.id_,
        title=tag_name,
        navbar=get_navbar(None),
        sidebar=gen_sidebar()
    )


@app.route("/archives/<int:year>/<int:month>", methods=["GET"])
def archives_year_month_get(year, month):
    articles = Article.query.filter(Article.date_time_.between("%04d-%02d" % (year, month),
                                                               "%04d-%02d" % (year, month + 1))).all()
    return render_template("archives.html",
                           articles=articles,
                           navbar=get_navbar(None),
                           sidebar=gen_sidebar())
