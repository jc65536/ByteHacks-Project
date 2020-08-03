from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from datetime import datetime, timedelta
import jwt

from .models import User
from .extensions import db

auth = Blueprint("auth", __name__)

@auth.route('/api/verify-token', methods=["POST"])
@cross_origin(supports_credentials=True)
def verify_token():
    auth_headers = request.headers.get('Authorization', '').split()

    invalid_msg = {
        'message': 'Invalid token. Registration and / or authentication required',
        'authenticated': False
    }
    expired_msg = {
        'message': 'Expired token. Reauthentication required.',
        'authenticated': False
    }
    success_msg = { 'authenticated': True }

    if len(auth_headers) != 2:
        return jsonify(invalid_msg), 401

    try:
        token = auth_headers[1]
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = User.query.filter_by(email=data['sub']).first()
        if not user:
            raise RuntimeError('User not found')
        return jsonify(success_msg)
    except jwt.ExpiredSignatureError:
        return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
    except (jwt.InvalidTokenError, Exception) as e:
        print(e)
        return jsonify(invalid_msg), 401

@auth.route('/api/login', methods=["GET", "POST"])
@cross_origin()
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
        'exp': datetime.utcnow() + timedelta(weeks=1),
        'name': user.name
    },
        current_app.config['SECRET_KEY']
    )

    return jsonify({'token': token.decode('UTF-8'), 'authenticated': True})


@auth.route('/api/register', methods=['POST'])
@cross_origin()
def signup():
    data = request.get_json()
    email_check = User.query.filter_by(email=data['email']).first()
    if email_check:
        return jsonify({'message': 'Email already exists in database', 'registered': False, 'error': 'email-duplicate'})
    new_user = User(name=data['name'], email=data['email'], password=data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'success', 'registered': True})
