# File: extensions.py
# Will mainly serve as a place to put database stuff, to prevent circular imports

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
