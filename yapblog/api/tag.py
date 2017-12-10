"""
/api/tag                    GET, POST
/api/tag/<tag.id>           GET, DELETE
/api/tag/articles/<tag.id>  GET
/api/tag/tags/<article.id>  GET
"""

from flask import request
from yapblog import app, db
from yapblog.models import Tag, Article
from yapblog.lib.api import ok, not_ok
from sqlalchemy.exc import IntegrityError


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
    Add the tag with name of tag_name.

    Method: POST

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True
        "id": <new_tag.id>
        "name": <new_tag.name>
    }
    """
    data = request.get_json()
    try:
        name = data["name"]
    except KeyError:
        return not_ok()
    new_tag = Tag(name)
    db.session.add(new_tag)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return not_ok()
    return ok(id=new_tag.id_, name=new_tag.name_)


@app.route("/api/tag/<int:tag_id>", methods=["GET"])
def api_tag_tag_id_get(tag_id):
    """
    GET the info of the tag with the id of tag_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True
        "id": <tag.id>
        "name": <tag.name>
    }
    """
    tag = Tag.query.filter_by(id_=tag_id)
    if tag is None:
        return not_ok()
    return ok(id=tag.id_, name=tag.name_)


@app.route("/api/tag/<int:tag_id>", methods=["DELETE"])
def api_tag_tag_id_delete(tag_id):
    """
    Delete the tag with id of tag_id.

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
    tag = Tag.query.filter_by(id_=tag_id)
    if tag is None:
        return not_ok()
    tag.delete()
    db.session.commit()
    return ok()


@app.route("/api/tag/articles/<int:tag_id>", methods=["GET"])
@app.route("/api/tag/<int:tag_id>/articles", methods=["GET"])
def api_tag_articles_tag_id(tag_id):
    """
    Get the article list with the tag of tag_id.

    Method: GET

    :return:
    Error:
    {
        "ok": False
    }
    Success:
    {
        "ok": True,
        "articles":
        [{
            "id": <article.id>,
            "title": <article.title>,
            "date_time": <aritcle.date_time>,
        }]
    }
    """
    tag = Tag.query.filter_by(id_=tag_id).first()
    if tag is None:
        return not_ok()
    print(tag.articles)
    return ok(articles=[{
        "id": article.id_,
        "title": article.title_,
        "date_time": "%04d-%02d-%02d" % (article.date_time_.year, article.date_time_.month, article.date_time_.day)
    } for article in tag.articles])


@app.route("/api/tag/tags/<int:article_id>", methods=["GET"])
def api_tag_tags_article_id(article_id):
    """
    Get the tag list of the article of article_id.

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
