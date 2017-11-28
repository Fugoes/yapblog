from yapblog import app
from yapblog.models import Comment
from yapblog.lib.api import not_ok, ok


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
    if comment.user is None:
        author_name = "Deleted User"
    else:
        author_name = comment.user.name_
    return ok(text=comment.text_,
              author_name=author_name)
