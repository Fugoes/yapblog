```
User( id, name, email, passwd_hash, is_admin )
Article( id, User.id author_id, date, title, Content.id html_content )
Tag( id, value )
Content( id, value )
Comment( id, value, Comment.id parent )

ArticleTag( Article.id, Tag.id )
ArticleComment( Article.id, Comment.id )
```
