from app import db


class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nickname = db.Column(db.String(16), index=True, unique=True)
        email = db.Column(db.String(128), index=True, unique=True)

        def __repr__(self):
            return '<User %r>' % self.nickname
