import requests
import json
import yapblog.config as config

url = "http://%s:%d/api/user/register" % (config.HOST, config.PORT)

for i in range(5):
    r = requests.post(url, data={
        "name": "test%d" % i,
        "email": "test%d@example.com" % i,
        "passwd": "test"
    })
    result = json.loads(r.content.decode())
    print(result)
    assert result["ok"]
