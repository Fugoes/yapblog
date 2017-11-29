import requests
import json
from yapblog import db
from yapblog.models import Tag, Article
import yapblog.config as config

url = "http://%s:%d/api/tag" % (config.HOST, config.PORT)

# test api_tag_get()
r = requests.get(url)
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

# test api_tag_post()

# test api_tag_delete()

# test api_tag_articles_tag_name(tag_name)
for i in range(10):
    r = requests.get(url + "/articles/%d" % i)
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]

# api_tag_tags_article_id(article_id)
for i in range(1, 4):
    r = requests.get(url + "/tags/%d" % i)
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]