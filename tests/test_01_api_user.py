import requests
import yapblog.config as config

url = "http://%s:%d/api/user/register" % (config.HOST, config.PORT)

for i in range(10):
    r = requests.post(url, data={
        "name": "test%d" % i,
        "email": "test%d@example.com" % i,
        "passwd": "test"
    })
    print(r.content.decode())
