#!/usr/bin/env python3

from sys import argv


def print_help():
    print("manage.py create-tables")
    print("          drop-tables")
    print("          help")


if len(argv) == 2:
    if argv[1] == "create-tables":
        from yapblog import db
        from yapblog.models import *

        db.create_all()
    elif argv[1] == "drop-tables":
        from yapblog import db
        from yapblog.models import *

        db.drop_all()
    elif argv[1] == "help":
        print_help()
    else:
        print_help()
else:
    print_help()
