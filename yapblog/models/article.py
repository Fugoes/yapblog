from yapblog import db


class Article(db.Model):
    # Primary key
    _id = db.Column("id", db.Integer, primary_key=True)
    # Foreign keys
    _author_id = db.Column(
        "author_id", db.Integer, db.ForeignKey("user.id"),
        nullable=False)
    _html_content_id = db.Column(
        "html_content_id", db.Integer, db.ForeignKey("content.id"),
        nullable=False)
    _page_id = db.Column(
        "page_id", db.Integer, db.ForeignKey("page.id"),
        nullable=False)
    # Properties
    _date = db.Column("date", db.DateTime, nullable=False)
    _title = db.Column("title", db.String(1024), nullable=False)


class Content(db.Model):
    # Primary key
    _id = db.Column("id", db.Integer, primary_key=True)
    # Properties
    _value = db.Column("value", db.Text, nullable=False)


class ArticleTag(db.Model):
    _article_id = db.Column("article_id", db.ForeignKey("article.id"), db.Integer, nullable=False)
    _tag_id = db.Column("tag_id", db.ForeignKey("tag.id"), db.Integer, nullable=False)


class Page(db.Model):
    # Primary Key
    _id = db.Column("id", db.Integer, primary_key=True)


class Comment(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    _value = db.Column("value", db.Text, nullable=False)


class CommentReply(db.Model):
    _id = db.Column("id", db.ForeignKey("comment.id"), db.Integer, nullable=False, unique=True)
    _reply_to_id = db.Column("reply_to_id", db.ForeignKey("comment.id"), db.Integer, nullable=False)
