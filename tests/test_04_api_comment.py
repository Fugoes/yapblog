import json
import requests
import yapblog.config as config

url = "http://%s:%d" % (config.HOST, config.PORT)

s = requests.Session()
r = s.post(url + "/api/user/login", json={
    "name": "debug",
    "passwd": "debug"
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = s.get(url + "/api/user/me")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = s.post(url + "/api/page/1/comments", json={
    "text": "ROOT",
    "reply_to_id": None,
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

root_id = result["id"]
r = s.post(url + "/api/page/1/comments", json={
    "text": "LEFT CHILD",
    "reply_to_id": root_id,
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = s.post(url + "/api/page/1/comments", json={
    "text": "RIGHT CHILD",
    "reply_to_id": root_id,
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = s.get(url + "/api/page/1/comments")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

comments = dict()
roots = []
for i in result["comments"]:
    if i["reply_to_id"] is None:
        roots.append(i["id"])
    else:
        try:
            comments[i["reply_to_id"]].append(i["id"])
        except KeyError:
            comments[i["reply_to_id"]] = [i["id"]]

for i in roots:
    r = s.get(url + "/api/comment/%d" % i)
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]
    for j in comments[i]:
        r = s.get(url + "/api/comment/%d" % j)
        result = json.loads(r.content.decode())
        print(result)
        assert result["ok"]

r = requests.delete(url + "/api/comment/1")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]
r = requests.delete(url + "/api/comment/2")
result = json.loads(r.content.decode())
print(result)
assert result["ok"]
