# yapblog

`yapblog` is acronym for `yet another personal blog`.

# Requirement

Please install `python3` with `flask`,`flask-login` and `flask-sqlalchemy` installed.

Please install `pandoc` for converting markdown to html.

# 项目结构

+ `yapblog/api/` : API
+ `yapblog/lib/` : 一些有用的函数
+ `yapblog/models/` : 与数据库的接口类，比如用户类 User
+ `yapblog/static/` : 静态文件
+ `yapblog/templates/` : 模板文件
+ `yapblog/views/` : 各个页面
+ `yapblog/config.py` : 配置文件
+ `tests/` : 测试

# `/api`

API 采用的模式是使用 JSON 来请求，并返回一个 JSON 格式的数据。使用的例子可以参考各个页面的模板文件。

## `/api/user`
与单个用户相关的接口，具体的参数与返回值参考 `yapblog.api.user` ：

+ `/api/user`
+ `/api/user/register`
+ `/api/user/login`
+ `/api/user/logout`

# `/register`
注册页面。

# `/login`
登录页面。

# `/logout`
登出页面。

# `/user`
用户信息页面。
