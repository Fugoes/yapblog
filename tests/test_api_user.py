import requests
import yapblog.config as config

url = "http://%s:%d/api/user" % (config.HOST, config.PORT)

r = requests.post(url, data={"name": "test", "email": "test@example.com", "passwd": "test"})
print(r.content.decode())
for i in range(1000):
    r = requests.post(url, data={
        "name": "test%d" % i,
        "email": "test%d@example.com" % i,
        "passwd": "test"
    })
