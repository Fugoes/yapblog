from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import yapb.config as config

# Init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SESSION_TYPE"] = config.SESSION_TYPE
app.config["SECRET_KEY"] = config.SECRET_KEY
# Init database
db = SQLAlchemy(app)
# Init login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# Load all models
from yapb.models import *
# Load all views
from yapb.views import *


@login_manager.user_loader
def load_user(user_id):
    """ Required by flask_login """
    user_id = int(user_id)
    return User.query.filter_by(id=user_id).first()
