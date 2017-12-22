from yapblog import app, db
from yapblog.lib.api import not_ok, ok
from yapblog.lib.auth import admin_api
from yapblog.models import Comment
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
