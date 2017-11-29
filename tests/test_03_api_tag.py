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

# test api_tag_tag_id(tag_id)
for i in range(1, 11):
    r = requests.get(url + "/%d" % i)
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]

# api_tag_article_id(article_id)
for i in range(1, 4):
    r = requests.get(url + "/%d" % i)
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]