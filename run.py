#!/usr/bin/env python3

from yapblog import app, db
from yapblog.models import User
import yapblog.config as config
from yapblog.lib.auth import md5_with_salt

user = User("debug", "debug@example.com", md5_with_salt("debug"))
db.session.add(user)
try:
    db.session.commit()
except Exception:
    pass

app.run(
    host=config.HOST,
    port=config.PORT,
    debug=config.DEBUG,
)
