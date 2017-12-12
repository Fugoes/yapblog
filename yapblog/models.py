"""
Database interface
"""

__all__ = ["Tag", "Page", "Article", "Comment", "User", "Category"]

from yapblog import db
from yapblog import config


class Category(db.Model):
    __tablename__ = "categories"
    # Attribute
    id_ = db.Column("id", db.Integer, db.Sequence("category_id_seq"), primary_key=True)
    name_ = db.Column("name", db.String(1024), unique=True, nullable=False)
    # Relationship
    articles = db.relationship("Article", back_populates="category", uselist=True)

    def __init__(self, name):
        self.name_ = name


tag_and_article = db.Table("tag_and_article",
                           db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
                           db.Column("article_id", db.Integer, db.ForeignKey("articles.id")))


class Tag(db.Model):
    __tablename__ = "tags"
    # Attribute
    id_ = db.Column("id", db.Integer, db.Sequence("tag_id_seq"), primary_key=True)
    name_ = db.Column("name", db.String(1024), unique=True, nullable=False)
    # Relationship
    articles = db.relationship("Article", secondary=tag_and_article, back_populates="tags")

    def __init__(self, name):
        self.name_ = name

    def __str__(self):
        return "<Tag id=%d name='%s'>" % (self.id_, self.name_)

    def __repr__(self):
        return self.__str__()


class Page(db.Model):
    __tablename__ = "pages"
    # Attribute
    id_ = db.Column("id", db.Integer, db.Sequence("page_id_seq"), primary_key=True)
    # Relationship
    comments = db.relationship("Comment", back_populates="page", uselist=True)

    def __init__(self):
        return

    def __str__(self):
        return "<Page id=%d>" % self.id_

    def __repr__(self):
        return self.__str__()


class Article(db.Model):
    __tablename__ = "articles"
    # Attribute
    id_ = db.Column("id", db.Integer, db.Sequence("article_id_seq"), primary_key=True)
    title_ = db.Column("title", db.String(1024), unique=True, nullable=False)
    date_time_ = db.Column("date_time", db.DateTime)
    html_content_ = db.Column("html_content", db.Text)
    markdown_content_ = db.Column("markdown_content", db.Text)
    img_url_ = db.Column("img_url", db.String(1024))
    # Foreign key
    page_id_ = db.Column("page_id", db.Integer, db.ForeignKey("pages.id"), nullable=True)
    category_id_ = db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), nullable=True)
    # Relationship
    page = db.relationship("Page", uselist=False)
    tags = db.relationship("Tag", secondary=tag_and_article, back_populates="articles")
    category = db.relationship("Category", back_populates="articles", uselist=False)

    def __init__(self, title, date_time, html_content, markdown_content, img_url=None):
        self.title_ = title
        self.date_time_ = date_time
        self.html_content_ = html_content
        self.markdown_content_ = markdown_content
        self.img_url_ = img_url if img_url else config.DEFAULT_BACKGROUND

    def __str__(self):
        return "<Article id=%d title='%s'>" % (self.id_, self.title_)

    def __repr__(self):
        return self.__str__()


class Comment(db.Model):
    __tablename__ = "comments"
    # Attribute
    id_ = db.Column("id", db.Integer, db.Sequence("comment_id_seq"), primary_key=True)
    text_ = db.Column("text", db.Text, nullable=False)
    is_deleted_ = db.Column("is_deleted", db.Boolean, nullable=False)
    # Foreign key
    reply_to_id_ = db.Column("reply_to_id", db.Integer, db.ForeignKey("comments.id"), nullable=True)
    page_id_ = db.Column("page_id", db.Integer, db.ForeignKey("pages.id"), nullable=True)
    user_id_ = db.Column("user_id", db.Integer, db.ForeignKey("users.id"), nullable=True)
    # Relationship
    replies = db.relationship("Comment", uselist=True)
    reply_to = db.relationship("Comment", remote_side=id_, uselist=False)
    page = db.relationship("Page", back_populates="comments", uselist=False)
    user = db.relationship("User", back_populates="comments", uselist=False)

    def __init__(self, text):
        self.text_ = text
        self.is_deleted_ = False

    def __str__(self):
        return "<Comment id=%d text='%s' is_deleted='%s'>" % (self.id_, self.text_, self.is_deleted_)

    def __repr__(self):
        return self.__str__()


class User(db.Model):
    __tablename__ = "users"
    id_ = db.Column("id", db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    name_ = db.Column("name", db.String(100), unique=True)
    email_ = db.Column("email", db.String(100), unique=True)
    passwd_hash_ = db.Column("passwd_hash", db.String(32))
    is_admin_ = db.Column("is_admin", db.Boolean, nullable=False)
    # Relationship
    comments = db.relationship("Comment", back_populates="user", uselist=True)

    def __init__(self, name, email, passwd_hash, is_admin=False):
        self.name_ = name
        self.email_ = email
        self.passwd_hash_ = passwd_hash
        self.is_admin_ = is_admin

    @property
    def is_active(self):
        """ Require by flask_login """
        return True

    @property
    def is_authenticated(self):
        """ Require by flask_login """
        return self.id_ is not None

    @property
    def is_anonymous(self):
        """ Require by flask_login """
        return False

    def get_id(self):
        """ Require by flask_login """
        return str(self.id_)

    def __str__(self):
        return "<User id=%d name='%s'>" % (self.id_, self.name_)

    def __repr__(self):
        return self.__str__()
