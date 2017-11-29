"""
run this test after running test_00.
"""

import requests
import json
from yapblog import db
from yapblog.models import Tag, Article
import yapblog.config as config

url = "http://%s:%d/api/tag" % (config.HOST, config.PORT)

# api_tag_get()
r = requests.get(url)
result = json.loads(r.content.decode())
print(result)
assert result["ok"]


# api_tag_post()
r = requests.post(url, json={
    "name": "test_tag"
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url)
result = json.loads(r.content.decode())
print(result)
assert result["ok"]


# api_tag_articles_tag_id(tag_id)
for i in range(1, 11):
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

# test api_tag_tag_id_delete(tag_id)
r = requests.delete(url + "/1")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url)
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url + "/tags/1")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]