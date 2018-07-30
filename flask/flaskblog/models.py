from time import time
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Sessions', backref='author', lazy=True)
    def __repr__(self):
        return "User({}, {})".format(self.username,self.email)


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Float, nullable=False, default=time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return "{}".format(self.times)
