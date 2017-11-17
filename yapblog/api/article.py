__all__ = ["api_article_new"]

import datetime
from flask import request
from yapblog import app
from yapblog.models import Article
from yapblog.lib.api import ok, not_ok
import yapblog.lib.regex as regex


@app.route("/api/article/<int:article_id>", methods=["GET"])
def api_article_article_id(article_id):
    """
    Get article with id of article_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "title": <article.title>,
        "date": <article.date>,
        "html_content": <article.html_content>,
        "page_id": <article.page_id>
    }
    """
    article = Article.query.filter_by(id_=article_id).first()
    if article is None:
        return not_ok()
    date = article.date_
    return ok(title=article.title_,
              date="%04d-%02d-%02d" % (date.year, date.month, date.day),
              html_content=article.html_content_,
              page_id=article.page_id_)


@app.route("/api/article", methods=["GET"])
def api_article():
    """
    Get all articles info.

    Method: GET

    Parameter:

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "articles":
        [
            {
                "id": <id of article>,
                "title": <title of article>
            },
        ]
    }
    """
    articles = Article.query.all()
    return ok(articles=[
        {
            "id": article.id_,
            "title": article.title_
        }
        for article in articles])


@app.route("/api/article/new", methods=["POST"])
def api_article_new():
    """
    Create a new article.

    Method: POST

    Parameter: title, date, html_content
    example:
        {
            "title": "Hello World",
            "date": "2017-10-01",
            "html_content": ""
        }

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "id": <id of new article>
    }
    """
    data = request.get_json()
    try:
        date = datetime.date(*tuple(map(int, regex.date.fullmatch(data["date"]).groups())))
    except AttributeError:
        return not_ok()
    try:
        title = data["title"]
        html_content = data["html_content"]
    except KeyError:
        return not_ok()
    article = Article.new(title, date, html_content)
    if article is None:
        return not_ok()
    return ok(id=article.id_)
