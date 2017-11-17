import json
import requests
import yapblog.config as config

url = "http://%s:%d/api/article" % (config.HOST, config.PORT)

r = requests.post(url + "/new", json={
    "title": "Hello World",
    "date": "2017-1-1",
    "html_content": "<h1>Hello World!</h1>"
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
assert not result["ok"]
