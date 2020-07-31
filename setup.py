from app import create_app
from app.extensions import db
db.create_all(app=create_app())
