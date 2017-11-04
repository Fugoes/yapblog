import requests
import yapb.config as config

url = "http://%s:%d/api/user" % (config.HOST, config.PORT)

r = requests.post(url, data={"name": "user1", "email": "user1@example.com"})
print(r)
