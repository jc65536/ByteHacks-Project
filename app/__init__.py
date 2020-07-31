from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Basic app factory
def create_app():
    app = Flask(__name__)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    from .extensions import db
    # Will probably need to make a separate config file at some point
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


def register_blueprints(app):
    from .main import main
    app.register_blueprint(main)
