__all__ = ["Comment"]

from yapblog import db


class Comment(db.Model):
    __tablename__ = "comments"
    # Primary key
    id_ = db.Column("id", db.Integer, db.Sequence("comment_id_seq"), primary_key=True)
    # Properties
    text_ = db.Column("text", db.Text, nullable=False)
    # Many to One
    reply_to_id_ = db.Column("reply_to_id", db.Integer, db.ForeignKey("comments.id"), nullable=True)
    page_id_ = db.Column("page_id", db.Integer, db.ForeignKey("pages.id"), nullable=True)
    # Relations
    replies_ = db.relationship("Comment", uselist=True)
    reply_to_ = db.relationship("Comment", remote_side=id_, uselist=False)
    page_ = db.relationship("Page",
                            uselist=False,
                            back_populates="comments_")

    def __init__(self, text):
        self.text_ = text


class Page(db.Model):
    __tablename__ = "pages"
    # Primary key
    id_ = db.Column("id", db.Integer, db.Sequence("page_id_seq"), primary_key=True)
    comments_ = db.relationship("Comment",
                                uselist=True,
                                back_populates="page_")

    def __init__(self):
        return

    @staticmethod
    def new():
        new_page = Page()
        db.session.add(new_page)
        db.session.commit()
        return new_page
