import json
import requests
import yapblog.config as config

url = "http://%s:%d/api/article" % (config.HOST, config.PORT)

content = """
<p>The <code>tests/</code> folder are tests for JSON APIs. All tests assume that the database is empty. If the test failed, it will throw <code>AssertionError</code> exception.</p>
<p>To run a test, first delete the old database (if any) and create a new empty database file:</p>
<span class="ex">python3</span> manage.py create-database</code></pre></div>
<p>Then start the server, and run the test:</p>
<div class="sourceCode"><pre class="sourceCode bash"><code class="sourceCode bash"><span class="ex">python3</span> -m tests.test_02_api_article</code></pre></div>
"""

r = requests.post(url + "/new", json={
    "title": "Hello World",
    "date": "2017-1-1",
    "html_content": content,
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
