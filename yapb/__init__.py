from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import yapb.config as config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "test"
