from yapblog import app, db
from yapblog.models import Comment
from yapblog.lib.api import not_ok, ok
from sqlalchemy.exc import IntegrityError


@app.route("/api/comment/<int:comment_id>", methods=["GET"])
def api_comment_comment_id(comment_id):
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
        comment_text = "Comment already deleted"
    else:
        comment_text = comment.text_
    if comment.user is None:
        author_name = "Deleted User"
    else:
        author_name = comment.user.name_
    return ok(text=comment_text,
              author_name=author_name)


@app.route("/api/comment/delete/<int:comment_id>", methods=["DELETE"])
def api_comment_delete_comment_id(comment_id):
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
