import requests
import json
import yapblog.config as config

url = "http://%s:%d/api/user" % (config.HOST, config.PORT)

for i in range(5):
    r = requests.post(url, json={
        "name": "test%d" % i,
        "email": "test%d@example.com" % i,
        "passwd": "test"
    })
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]

r = requests.get(url)
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url + "/1")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.delete(url + "/2")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.get(url + "/2")
result = json.loads(r.content.decode())
print(result)
assert not result["ok"]
