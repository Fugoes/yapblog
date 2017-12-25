from flask import request
from yapblog import app, db
from yapblog.lib.api import not_ok, ok
from yapblog.lib.auth import admin_api
from yapblog.models import Comment, User
from sqlalchemy.exc import IntegrityError


@app.route("/api/comment/<int:comment_id>", methods=["GET"])
def api_comment_comment_id_get(comment_id):
    """

    :param comment_id:
    :return:
    {
        "ok": True,
        "text": <comment's text>,
        "author_name": <comment's author's name>
    }
    """
    comment = Comment.query.filter_by(id_=comment_id).first()
    if comment is None:
        return not_ok()
    if comment.is_deleted_:
        comment_text = "Deleted Comment"
    else:
        comment_text = comment.text_
    if comment.user is None:
        author_name = "Deleted User"
    else:
        author_name = comment.user.name_
    return ok(text=comment_text,
              author_name=author_name)


@app.route("/api/comment/<int:comment_id>", methods=["DELETE"])
@admin_api
def api_comment_comment_id_delete(comment_id):
    comment = Comment.query.filter_by(id_=comment_id).first()
    if comment is None:
        return not_ok()
    comment.is_deleted_ = True
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return not_ok()
    return ok(id=comment.id_, is_deleted=comment.is_deleted_)


@app.route("/api/comment", methods=["GET"])
@admin_api
def api_comment():
    author_match = request.args.get("author_match")
    text_match = request.args.get("text_match")
    query_args = []
    if author_match and len(author_match) > 0:
        query_args.append(Comment.user.has(User.name_.contains(author_match)))
    if text_match and len(text_match) > 0:
        query_args.append(Comment.text_.contains(text_match))
    if len(query_args) == 0:
        comments = Comment.query.all()
    else:
        comments = Comment.query.filter(*query_args).all()
    return ok(comments=[{
        "id": comment.id_,
        "author": {
            "name": comment.user.name_,
            "id": comment.user.id_,
        },
        "text": comment.text_,
        "is_deleted": comment.is_deleted_,
        "page_id": comment.page_id_,
    } for comment in comments])
