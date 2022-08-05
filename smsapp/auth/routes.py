from flask import render_template, redirect

from smsapp.auth import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html', title="Login")
@auth.route('/register')
def register():
    return render_template('auth/register.html', title="Register")
@auth.route('/logout')
def logout():
    return render_template('auth/logout.html', title="Logout")
