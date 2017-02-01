from app import db
from app import lm
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=True, unique=True)
    nickname = db.Column(db.String(16), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname


@lm.user_loader
def load_user(id):
    u = User.query.get(int(id))
    return u


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body


