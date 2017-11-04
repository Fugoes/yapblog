from yapb import db, login_manager
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
        return {"name": self.name, "email": self.email, "id": self.id, "passwd_hash": self.passwd_hash}

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.id is not None

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
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


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    return User.query.filter_by(id=user_id).first()
