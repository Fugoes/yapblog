__all__ = ["index"]

from flask import render_template, Markup, redirect
from yapblog import app, config, db
from yapblog.models import Article, Tag
from yapblog.lib.page import SideBar, get_navbar, get_archives, archives_data


def gen_sidebar():
    return SideBar(items=[
        SideBar.gen_tag_list(),
        get_archives(),
    ])


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        articles=Article.query.order_by(db.desc(Article.date_time_)).all(),
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
    return render_template("tag_by_name.html",
                           articles=tag.articles,
                           tag_id=tag.id_,
                           title=tag_name,
                           navbar=get_navbar("Tags"),
                           sidebar=gen_sidebar())


@app.route("/tags", methods=["GET"])
def tags_get():
    tags = Tag.query.all()
    tag_and_articles = []
    for tag in tags:
        articles = tag.articles
        count = len(articles)
        if count > 0:
            tag_and_articles.append((tag, count, articles))
    return render_template("tag.html",
                           tag_and_articles=tag_and_articles,
                           title="Tags",
                           navbar=get_navbar("Tags"),
                           sidebar=gen_sidebar())


@app.route("/archives/<int:year>/<int:month>", methods=["GET"])
def archives_year_month_get(year, month):
    articles = Article.query.filter(Article.date_time_.between("%04d-%02d" % (year, month),
                                                               "%04d-%02d" % (year, month + 1))).all()
    count = len(articles)
    return render_template("archives.html",
                           time_and_posts=[((year, month), count, articles)],
                           navbar=get_navbar("Archives"),
                           sidebar=gen_sidebar())


@app.route("/archives", methods=["GET"])
def archives_get():
    time_and_posts = []
    for (year, month), group in archives_data():
        articles = list(group)
        count = len(articles)
        time_and_posts.append(((year, month), count, articles))
    return render_template("archives.html",
                           time_and_posts=time_and_posts,
                           navbar=get_navbar("Archives"),
                           sidebar=gen_sidebar())
