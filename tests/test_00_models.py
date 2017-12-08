from datetime import datetime
from yapblog import db
from yapblog.models import Tag, Page, Article, Comment, User

db.drop_all()
db.create_all()

content = """<h1>My First Post</h1>
<h2>My First Post</h2>
<p>This is my first Post!</p>
<p>I could have <code>code</code>, <emph>emph</emph></p>
<p>I could quote something here,</p>
<blockquote class="blockquote">
  <p class="mb-0">Life is hard, but sexy.</p>
</blockquote>
<p>I could put codes here,</p>
<pre><code>def hello_world():
    print("Hello World!")
</pre></code>
<p>And maybe a table,</p>
<table class="table">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>"""

print("Creating tags")
tags = [Tag("%d" % i) for i in range(10)]

print("Creating articles")
pages = [Page() for _ in range(3)]
articles = [Article("Hello World%d" % i, datetime(2017, 10, 10), content, "") for i in range(3)]
for article, page in zip(articles, pages):
    article.page = page
article0 = articles[0]

print("Add tags to the first article")
for tag in tags:
    article0.tags.append(tag)

db.session.add_all(tags)
db.session.add_all(articles)
db.session.commit()

print()
print("All tags:")
for i in Tag.query.all():
    print(i)
print()
print("All Articles and its tags and page:")
for i in Article.query.all():
    print("%s: %s %s" % (str(i), i.tags, i.page))

print()
print("Add comments to the first article")
comments = [Comment("Hello%d" % i) for i in range(10)]
for comment in comments:
    article0.page.comments.append(comment)

db.session.commit()
print()
print("All Articles and its comments:")
for i in Article.query.all():
    print("%s: %s" % (str(i), str(i.page.comments)))

print()
print("Set all comments reply to the first one")
for comment in comments[1:]:
    comments[0].replies.append(comment)
db.session.commit()

print()
print("The first comment and its replies")
print("%s: %s" % (comments[0], comments[0].replies))

c = Comment.query.filter_by(id_=comments[0].id_).first()
db.session.delete(c)
db.session.commit()

print()
print("All Articles and its comments:")
for i in Article.query.all():
    print("%s: %s" % (str(i), str(i.page.comments)))
