import json
import requests
import yapblog.config as config

url = "http://%s:%d/api/article" % (config.HOST, config.PORT)

content = """
<h1>My First Post</h1>
<h2>My First Post</h2>
<p>This is my first Post!</p>
<p>I could have <code>code</code>, <emph>emph</emph></p>
<p>I could quote something here,</p>
<blockquote class="blockquote">
  <p class="mb-0">Life is hard, but sexy.</p>
</blockquote>
<p>I could put codes here,</p>
<pre><code>def hello_world():
    print("Hello World!")
</pre></code>
<p>And maybe a table,</p>
<table class="table">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table> 
"""

r = requests.post(url + "/new", json={
    "title": "Hello World",
    "date": "2017-1-1",
    "html_content": content,
})
result = json.loads(r.content.decode())
print(result)
assert result["ok"]

r = requests.post(url + "/new", json={
    "title": "Hello World Again",
    "date": "2017-1-19",
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
assert result["ok"]
