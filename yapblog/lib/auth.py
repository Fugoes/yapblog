from hashlib import md5
from yapblog import config


def md5_with_salt(passwd):
    return md5((passwd + config.PASSWD_HASH_SALT).encode()).hexdigest()
