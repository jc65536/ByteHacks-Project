from flask import Flask
import os
from json import load
from flask_cors import CORS

SECRET_KEY = os.urandom(32)
YELP_API_KEY = os.environ['YELP_API_KEY']
print(repr(YELP_API_KEY))

# Basic app factory
def create_app():
    app = Flask(__name__)
    register_extensions(app)
    register_blueprints(app)
    cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

    return app


def register_extensions(app):
    from .extensions import db
    # Will probably need to make a separate config file at some point
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


def register_blueprints(app):
    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .models import User
