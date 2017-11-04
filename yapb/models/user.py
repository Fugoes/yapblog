from yapb import db
from hashlib import md5
import yapb.config as config


def md5_with_salt(passwd):
    return md5((passwd + config.PASSWD_HASH_SALT).encode()).hexdigest()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    passwd_hash = db.Column(db.String(32))

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd_hash = md5_with_salt(passwd)
        self.id = None

    def to_dict(self):
        return {"name": self.name, "email": self.email}

    @property
    def is_active(self):
        """ Require by flask_login """
        return True

    @property
    def is_authenticated(self):
        """ Require by flask_login """
        return self.id is not None

    @property
    def is_anonymous(self):
        """ Require by flask_login """
        return False

    def get_id(self):
        """ Require by flask_login """
        return str(self.id)

    def __repr__(self):
        return "<User %s>" % self.name

    def __str__(self):
        return "<User %s>" % self.name

    @staticmethod
    def get_user(**kwargs):
        query_dict = dict()
        try:
            query_dict["name"] = kwargs["name"]
        except KeyError:
            try:
                query_dict["email"] = kwargs["email"]
            except KeyError:
                return None

        try:
            query_dict["passwd_hash"] = md5_with_salt(kwargs["passwd"])
        except KeyError:
            return None

        users = User.query.filter_by(**query_dict)
        if len(list(users)) == 1:
            return users.first()
        else:
            return None
