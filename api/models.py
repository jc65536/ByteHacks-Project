from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            print("Email, Password:", email, password)
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            print("Username, Password_Hash_Validity", email, check_password_hash(user.password, password))
            print(user.password, password, generate_password_hash(password))
            return None
        return user


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
