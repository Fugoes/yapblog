#!/usr/bin/env python3

from sys import argv


def help():
    print("manage.py create-database")
    print("          help")


if len(argv) == 2:
    if argv[1] == "create-database":
        from yapblog import db
        from yapblog.models import *

        db.create_all()

    elif argv[1] == "help":
        help()
    else:
        help()
else:
    help()
