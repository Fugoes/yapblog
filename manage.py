#!/usr/bin/env python3

from sys import argv
from yapblog.lib.auth import md5_with_salt
import yapblog.config as config


def print_help():
    print("manage.py create-tables")
    print("          drop-tables")
    print("          database-shell")
    print("          help")


if len(argv) == 2:
    if argv[1] == "create-tables":
        from yapblog import db
        from yapblog.models import *

        db.create_all()
        db.session.add(User(name=config.ADMIN_USER_NAME,
                            email=config.ADMIN_USER_EMAIL,
                            passwd_hash=md5_with_salt(config.ADMIN_USER_PASSWORD)))

    elif argv[1] == "drop-tables":
        from yapblog import db
        from yapblog.models import *

        db.drop_all()

    elif argv[1] == "database-shell":
        from yapblog import db
        from yapblog.models import *
        from IPython import embed

        embed()

    elif argv[1] == "help":
        print_help()

    else:
        print_help()

else:
    print_help()
