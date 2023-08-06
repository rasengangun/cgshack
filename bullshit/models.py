from bullshit import db
from flask_login import UserMixin


class Lay (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(100),nullable=False)
    photo = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'