__all__ = ["Article", "Page", "Comment"]

from sqlalchemy.exc import IntegrityError
from yapblog import db


class Article(db.Model):
    __tablename__ = "article"
    # Primary key
    id_ = db.Column("id", db.Integer, primary_key=True)
    # Properties
    title_ = db.Column("title", db.String(1024), nullable=False, unique=True)
    date_ = db.Column("date", db.Date, nullable=False)
    html_content_ = db.Column("html_content", db.Text, nullable=False)
    # One to One
    page_id_ = db.Column(
        "page_id", db.Integer, db.ForeignKey("page.id"),
        nullable=False)

    def __init__(self, title, date, html_content, page_id):
        self.title_ = title
        self.date_ = date
        self.html_content_ = html_content
        self.page_id_ = page_id

    @staticmethod
    def new(title, date, html_content):
        new_page = Page.new()
        new_article = Article(title, date, html_content, new_page.id_)
        db.session.add(new_article)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return new_article


class Page(db.Model):
    __tablename__ = "page"
    # Primary key
    id_ = db.Column("id", db.Integer, primary_key=True)
    comments_ = db.relationship("Comment",
                                backref="page", lazy=True)

    def __init__(self):
        return

    @staticmethod
    def new():
        new_page = Page()
        db.session.add(new_page)
        db.session.commit()
        return new_page


class Comment(db.Model):
    __tablename__ = "comment"
    # Primary key
    id_ = db.Column("id", db.Integer, primary_key=True)
    # Properties
    text_ = db.Column("text", db.Text, nullable=False)
    # One to One
    reply_to_id_ = db.Column("reply_to_id", db.ForeignKey("comment.id"), nullable=True)
    # Many to One
    page_id_ = db.Column("page_id", db.Integer, db.ForeignKey("page.id"), nullable=True)
