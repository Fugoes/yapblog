"""
Examples for adding tags to article

    >>> t = Tag("Computer Science")
    >>> a = Article.query.filter_by(title_="Hello World").first()
    >>> a.tags_.append(t)
    >>> db.session.commit()

Deleting the first tag from article

    >>> a = Article.query.filter_by(title_="Hello World").first()
    >>> a.tags_.pop(0)
    >>> db.session.commit()

"""

__all__ = ["Article", "Page", "Tag"]

from sqlalchemy.exc import IntegrityError
from yapblog import db
from yapblog.models.comment import Page

tags_to_articles = db.Table("tags_to_articles",
                            # Left id
                            db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
                            # Right id
                            db.Column("article_id", db.Integer, db.ForeignKey("articles.id")))


class Tag(db.Model):
    __tablename__ = "tags"
    # Primary key
    id_ = db.Column("id", db.Integer, db.Sequence("tag_id_seq"), primary_key=True)
    # Value
    value_ = db.Column("value", db.String(1024), nullable=False)
    articles_ = db.relationship("Article",
                                secondary=tags_to_articles,
                                back_populates="tags_")

    def __init__(self, value):
        self.value_ = value


class Article(db.Model):
    __tablename__ = "articles"
    # Primary key
    id_ = db.Column("id", db.Integer, db.Sequence("article_id_seq"), primary_key=True)
    # Properties
    title_ = db.Column("title", db.String(1024), nullable=False, unique=True)
    date_ = db.Column("date", db.Date, nullable=False)
    html_content_ = db.Column("html_content", db.Text, nullable=False)
    # One to One
    page_id_ = db.Column(
        "page_id", db.Integer, db.ForeignKey("pages.id"),
        nullable=False)
    # Relations
    tags_ = db.relationship("Tag",
                            secondary=tags_to_articles,
                            back_populates="articles_")
    page_ = db.relationship("Page")

    def __init__(self, title, date, html_content):
        self.title_ = title
        self.date_ = date
        self.html_content_ = html_content

    @staticmethod
    def new(title, date, html_content):
        new_page = Page()
        new_article = Article(title, date, html_content)
        new_article.page_ = new_page
        db.session.add(new_article)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return new_article
