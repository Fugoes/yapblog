import requests
import yapb.config as config

url = "http://%s:%d/api/user" % (config.HOST, config.PORT)

r = requests.post(url, data={"name": "user1", "email": "user1@example.com", "passwd": "slkdfjalsdf"})
print(r)
r = requests.post(url, data={"name": "user2", "email": "user2@example.com", "passwd": "slkdxfjalsdf"})
print(r)
r = requests.post(url, data={"name": "test", "email": "test@example.com", "passwd": "test"})
print(r)
