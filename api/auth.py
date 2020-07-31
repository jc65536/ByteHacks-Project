from flask import Blueprint, flash, redirect, url_for, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from .models import User
from .extensions import db

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print("HERE")
        username_or_email = request.form.get("username_or_email")
        password = request.form.get("password")
        remember = True if request.form.get('remember_me') else False

        user = User.query.filter((User.email == username_or_email) | (User.username == username_or_email)).first()
        if not user or not check_password_hash(user.password, password):
            flash("Check your login details and try again.")
            print("Fail")
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # Testing
            next_page = url_for('main.success')
            print("Success!")
            # return jsonify({'username': user.username})
        return redirect(next_page)
    else:
        return render_template("testing_files/login.html")
        #return "Login Page Here"


@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print("New User: ", username, email, password)

        username_check = User.query.filter_by(username=username).first()

        if username_check:
            flash("Username Already Exists")
            return redirect(url_for('auth.signup'))

        email_check = User.query.filter_by(email=email).first()
        if email_check:
            flash("Email already exists")
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        # Testing
        return redirect(url_for('auth.login'))

        # return jsonify({'username': user.username})
    else:
        return render_template("testing_files/register.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged Out"
