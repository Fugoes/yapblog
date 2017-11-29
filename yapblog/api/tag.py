"""
/api/tag               GET, POST, DELETE
/api/tag/<tag.id>      GET
/api/tag/<article.id>  GET
"""

from flask import request
from yapblog import app, db
from yapblog.models import Tag, Article
from yapblog.lib.api import ok, not_ok


@app.route("/api/tag", methods=["GET"])
def api_tag_get():
    """
    Get an tag list of all the existed tags.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        [{
            "id": <tag.id>
            "name": <tag.name>
        }]
    }
    """
    tags = Tag.query.all()
    if tags is None:
        return not_ok()
    return ok(
        tags=[{
            "id": tag.id_,
            "name": tag.name_
        } for tag in tags])


@app.route("/api/tag", methods=["POST"])
def api_tag_post():
    """
    Add the tag (with name of tag_name) for the article (with the id of article_id).

    Method: POST

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
    pass


@app.route("/api/tag", methods=["DELETE"])
def api_tag_delete():
    """
    Delete the tag (with name of tag_name) of the article (with the id of article_id).

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
    pass


@app.route("/api/tag/<int:tag_id>", methods=["GET"])
def api_tag_tag_id(tag_id):
    """
    Get an article list with the tag of tag_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "tag_id": <tag.id>
        "tag_name": <tag.name>
        "articles":
        [{
            "id": <article.id>
            "title": <article.title>
        }]
    }
    """
    tag = Tag.query.filter_by(id_=tag_id).first()
    if tag is None:
        return not_ok()
    return ok(
        tag_id=tag.id_,
        tag_name=tag.name_,
        articles=[{
            "id": article.id_,
            "title": article.title_
        } for article in tag.articles])


@app.route("/api/tag/<int:article_id>", methods=["GET"])
def api_tag_article_id(article_id):
    """
    Get a tag list of the article of article_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "article_id": <article.id>
        "article_name": <article.title>
        "tags":
        [{
            "id": <tag.id>
            "title": <tag.name>
        }]
    }
    """
    article = Article.query.filter_by(id_=article_id).first()
    if article is None:
        return not_ok()
    return ok(
        article_id=article.id_,
        article_title=article.title_,
        tags=[{
            "id": tag.id_,
            "name": tag.name_
        } for tag in article.tags])
