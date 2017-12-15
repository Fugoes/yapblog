from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import time
import yapblog.config as config

# Init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SESSION_TYPE"] = config.SESSION_TYPE
app.config["SECRET_KEY"] = config.SECRET_KEY
# Init database
db = SQLAlchemy(app, session_options={"autoflush": False})
# Init login_manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# Load all models
from yapblog.models import *
# Load all views
from yapblog.views import *
# Load all apis
from yapblog.api import *

@app.before_request
def before_request():
    start_time = time.time()
    g.request_time = lambda: "%.6fs" % (time.time() - start_time)


@login_manager.user_loader
def load_user(user_id):
    """ Required by flask_login """
    user_id = int(user_id)
    return User.query.filter_by(id_=user_id).first()

