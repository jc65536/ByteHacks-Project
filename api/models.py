from .extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    positions = db.Column(db.Integer)
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    wage = db.Column(db.Float)
    employer = db.Column(db.String)
    creator = db.Column(db.String)
