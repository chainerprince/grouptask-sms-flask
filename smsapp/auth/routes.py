from smsapp import db
from flask import render_template, redirect, request, url_for, session
from smsapp.auth.forms import LoginForm, RegistrationForm
from smsapp.auth import auth
from smsapp.models import User
from flask_login import login_user, login_required, logout_user

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('main.chat_page')) 
    return render_template('auth/login.html', title="Login", form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print("User has been added")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title="Register", form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))