"""
/api/article              GET, POST
/api/article/<article.id> GET, DELETE
"""

__all__ = ["api_article_article_id_get", "api_article_article_id_delete", "api_article_get", "api_article_post"]

import datetime
from flask import request
from sqlalchemy.exc import IntegrityError
from yapblog import app, db
from yapblog.models import Article, Page
from yapblog.lib.api import ok, not_ok
import yapblog.lib.regex as regex


@app.route("/api/article/<int:article_id>", methods=["GET"])
def api_article_article_id_get(article_id):
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
        "date_time": <article.date>,
        "html_content": <article.html_content>,
        "page_id": <article.page_id>
    }
    """
    article = Article.query.filter_by(id_=article_id).first()
    if article is None:
        return not_ok()
    date_time = article.date_time_
    return ok(title=article.title_,
              date_time="%04d-%02d-%02d" % (date_time.year, date_time.month, date_time.day),
              html_content=article.html_content_,
              page_id=article.page_id_)


@app.route("/api/article/<int:article_id>", methods=["DELETE"])
def api_article_article_id_delete(article_id):
    """
    Delete the article with id of article_id.

    Method: DELETE

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True
    }
    """
    Article.query.filter_by(id_=article_id).delete()
    db.session.commit()
    return ok()


@app.route("/api/article", methods=["GET"])
def api_article_get():
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
                "title": <title of article>,
                "date_time": <date string of article>
            },
        ]
    }
    """
    articles = Article.query.all()
    return ok(articles=[
        {
            "id": article.id_,
            "title": article.title_,
            "date_time": "%04d-%02d-%02d" % (article.date_time_.year, article.date_time_.month, article.date_time_.day)
        }
        for article in articles])


@app.route("/api/article", methods=["POST"])
def api_article_post():
    """
    Create a new article.

    Method: POST

    Parameter: title, date, html_content
    example:
        {
            "title": "Hello World",
            "date_time": "2017-10-01",
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
        date_time = datetime.datetime(*tuple(map(int, regex.date.fullmatch(data["date_time"]).groups())))
    except AttributeError:
        return not_ok()
    try:
        title = data["title"]
        html_content = data["html_content"]
    except KeyError:
        return not_ok()
    new_article = Article(title, date_time, html_content)
    new_article.page = Page()
    db.session.add(new_article)
    try:
        db.session.commit()
    except IntegrityError:
        return not_ok()
    return ok(id=new_article.id_)