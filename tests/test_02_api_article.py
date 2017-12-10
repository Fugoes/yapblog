import json
import requests
import yapblog.config as config
from yapblog.models import Tag, Page, Article

url = "http://%s:%d/api/article" % (config.HOST, config.PORT)

content = """# Welcome to `YapBlog`

Yet Another Personal BLOG.

- It is markdown supported.
- And more...

## `YapBlog` support all markdown syntax

1. First
2. Second
3. Third

```python
print("Hello World")
```

> Life is hard, but sexy.

`monospace`, *emphasize*.

Firefox is a good browser.

![](http://www.hiapphere.com/data/icon/201711/org.mozilla.firefox_HiAppHere.com.png)
"""

r = requests.post(url, json={
    "title": "Hello World",
    "date_time": "2017-1-1",
    "markdown_content": content,
    "tags": ["YapBlog", "Test"]
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

for i in range(4):
    r = requests.post(url, json={
        "title": "Hello World Again%d" % i,
        "date_time": "2017-1-19",
        "markdown_content": content,
        "tags": ["YapBlog"]
    })
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]

r = requests.get(url + "/1")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url + "/2")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.patch(url + "/2", json={
    "tags": ["So", "What"]
})
result = json.loads(r.content.decode())
assert result["ok"]
