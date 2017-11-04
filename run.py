#!/usr/bin/env python3

from yapb import app
from yapb.views import *
from yapb.models import *

import yapb.config as config

app.run(
    host=config.HOST,
    port=config.PORT,
    debug=config.DEBUG,
)
