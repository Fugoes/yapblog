#!/usr/bin/env python3

from yapb import app
import yapb.config as config

app.run(
    host=config.HOST,
    port=config.PORT,
    debug=config.DEBUG,
)
