from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from oauth2 import OAuthSignIn

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
