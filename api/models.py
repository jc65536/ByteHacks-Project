from .extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    positions = db.Column(db.Integer)
    date = db.Column(db.Text)
    location = db.Column(db.Text)
    description = db.Column(db.Text)

    employer = db.Column(db.String)
