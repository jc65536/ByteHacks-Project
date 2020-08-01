from flask import Blueprint, flash, redirect, url_for, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from .models import User
from .extensions import db

auth = Blueprint("auth", __name__)


@auth.route('/api/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get('remember_me') else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid login credentials'})

        login_user(user, remember=remember)

        return jsonify({'message': 'success'})
    else:
        return render_template("testing_files/login.html")


@auth.route('/api/register', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        print("New User: ", name, email)

        email_check = User.query.filter_by(email=email).first()
        if email_check:
            return jsonify({'message': 'Email already exists in database'})
        new_user = User(username=name, email=email, password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'success'})
    else:
        return render_template("testing_files/register.html")


@auth.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'success'})
