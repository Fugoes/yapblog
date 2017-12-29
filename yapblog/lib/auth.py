from hashlib import md5
from flask import render_template
from flask_login import login_required, current_user
from functools import wraps
from yapblog.lib.api import not_ok
from yapblog import config
import random
import string


def gen_salt():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def md5_with_salt(passwd, salt):
    return md5((md5((passwd + config.PASSWD_HASH_SALT).encode()).hexdigest() + salt).encode()).hexdigest()


def admin_required(func):
    """
    Warning: This must work with @login_required
    """

    @login_required
    @wraps(func)
    def __decorator(*args, **kwargs):
        if current_user.is_admin_:
            return func(*args, **kwargs)
        else:
            return render_template("not_found.html", text="404 Not Found")

    return __decorator


def admin_api(func):
    def _func(*args, **kwargs):
        if not current_user.is_anonymous:
            if current_user.is_admin_:
                return func(*args, **kwargs)
        return not_ok()

    _func.__name__ = func.__name__
    return _func
