from hashlib import md5
from flask import render_template
from flask_login import login_required, current_user
from flask_login.utils import wraps
from yapblog import config


def md5_with_salt(passwd):
    return md5((passwd + config.PASSWD_HASH_SALT).encode()).hexdigest()


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
