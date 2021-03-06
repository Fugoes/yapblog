import datetime
from flask import render_template, Markup, redirect
from flask_login import current_user
from yapblog import app, config, db
from yapblog.models import Article, Tag, Category
from yapblog.lib.page import SideBar, get_navbar, get_archives, archives_data, get_categories


def gen_sidebar():
    return SideBar(items=[
        SideBar.gen_tag_list(),
        get_categories(),
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
                                   title=title + " - " + config.WEBSITE_NAME,
                                   article=article,
                                   html_content=Markup(article.html_content_),
                                   page_id=article.page_id_,
                                   user=None if current_user.is_anonymous else current_user,
                                   comment=True,
                                   navbar=get_navbar(None),
                                   sidebar=gen_sidebar())
    else:
        return redirect("/", code=404)


@app.route("/tags/<string:tag_name>", methods=["GET"])
def tags_tag_name(tag_name):
    tag = Tag.query.filter_by(name_=tag_name).first()
    tag_and_articles = []
    if tag is None:
        return redirect("/", code=404)
    else:
        articles = tag.articles
        count = len(articles)
        if count > 0:
            tag_and_articles.append((tag, count, articles))
        return render_template("tags.html",
                               tag_and_articles=tag_and_articles,
                               title="Tag: " + tag_name + " - " + config.WEBSITE_NAME,
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
    return render_template("tags.html",
                           tag_and_articles=tag_and_articles,
                           title="Tags" + " - " + config.WEBSITE_NAME,
                           navbar=get_navbar("Tags"),
                           sidebar=gen_sidebar())


@app.route("/categories", methods=["GET"])
def categories_get():
    category_and_articles = []
    for category in Category.query.all():
        articles = category.articles
        count = len(articles)
        if count > 0:
            category_and_articles.append((category, count, articles))
    return render_template("categories.html",
                           category_and_articles=category_and_articles,
                           title="Categories" + " - " + config.WEBSITE_NAME,
                           navbar=get_navbar("Categories"),
                           sidebar=gen_sidebar())


@app.route("/categories/<string:category_name>", methods=["GET"])
def categories_category_name(category_name):
    category = Category.query.filter_by(name_=category_name).first()
    category_and_articles = []
    if category is None:
        return render_template("not_found.html", text="")
    else:
        articles = category.articles
        count = len(articles)
        if count > 0:
            category_and_articles.append((category, count, articles))
        return render_template("categories.html",
                               category_and_articles=category_and_articles,
                               title="Category: " + category_name + " - " + config.WEBSITE_NAME,
                               navbar=get_navbar("Categories"),
                               sidebar=gen_sidebar())


@app.route("/archives/<int:year>/<int:month>", methods=["GET"])
def archives_year_month_get(year, month):
    articles = Article.query.filter(Article.date_time_.between(
        datetime.datetime(year, month, 1, 0, 0, 0),
        datetime.datetime(year, month + 1, 1, 0, 0, 0) if month < 12 else datetime.datetime(
            year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(days=1))).all()
    count = len(articles)
    monthname = datetime.datetime(year, month, 1, 0, 0, 0).strftime("%B")
    return render_template("archives.html",
                           title=monthname + ", " + str(year) + " - " + config.WEBSITE_NAME,
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
                           title="Archives" + " - " + config.WEBSITE_NAME,
                           time_and_posts=time_and_posts,
                           navbar=get_navbar("Archives"),
                           sidebar=gen_sidebar())
