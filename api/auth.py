from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import jwt

from .models import User
from .extensions import db

auth = Blueprint("auth", __name__)


@auth.route('/api/login', methods=["GET", "POST"])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']
    user = User.authenticate(email=email, password=password)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(weeks=1)},
        current_app.config['SECRET_KEY']
    )

    return jsonify({'token': token.decode('UTF-8')})


@auth.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json()
    email_check = User.query.filter_by(email=data['email']).first()
    if email_check:
        return jsonify({'message': 'Email already exists in database', 'registered': False})
    print("New User Password:", data['password'])
    new_user = User(name=data['name'], email=data['email'], password=data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'success'})
