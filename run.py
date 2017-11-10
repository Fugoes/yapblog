#!/usr/bin/env python3

from yapblog import app
import yapblog.config as config

app.run(
    host=config.HOST,
    port=config.PORT,
    debug=config.DEBUG,
)
