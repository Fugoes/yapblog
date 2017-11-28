from flask import request
from flask_login import current_user
from yapblog import app, db
from yapblog.models import Page, Comment
from yapblog.lib.api import ok, not_ok


@app.route("/api/page/<int:page_id>/comments", methods=["GET"])
def api_page_page_id_comments_get(page_id):
    page = Page.query.filter_by(id_=page_id).first()
    if page is None:
        return not_ok()
    else:
        return ok(comments=[{
            "id": comment.id_,
            "reply_to_id": comment.reply_to_id_
        } for comment in page.comments])


@app.route("/api/page/<int:page_id>/comments", methods=["POST"])
def api_page_page_id_comments_post(page_id):
    """
    text, reply_to_id

    :param page_id:
    :return:
    """
    if current_user.is_anonymous():
        return not_ok()
    else:
        data = request.get_json()
        try:
            text = data["text"]
            reply_to_id = data["reply_to_id"]
        except KeyError:
            return not_ok()
        new_comment = Comment(text)
        new_comment.reply_to = Comment.query.filter_by(id_=reply_to_id).first()
        if new_comment.reply_to.page.id_ != page_id:
            return not_ok()
        new_comment.page = Page.query.filter_by(id_=page_id).first()
        db.session.add(new_comment)
        db.session.commit()
        return ok(id=new_comment.id_)
