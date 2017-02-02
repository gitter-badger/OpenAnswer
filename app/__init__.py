from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

socketio = SocketIO()

app = Flask(__name__)
app.config.from_object('config')


socketio.init_app(app)

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = ''
from app import views, models
from app.chat import events

socketio.run(app)
