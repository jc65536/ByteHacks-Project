from flask import Flask, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

SECRET_KEY = os.urandom(32)


# Basic app factory
def create_app():
    app = Flask(__name__)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    from .extensions import db, login_manager
    # Will probably need to make a separate config file at some point
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


def register_blueprints(app):
    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .models import User

    from .extensions import login_manager

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
