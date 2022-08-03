from flask import render_template, redirect

from smsapp.auth import auth

@auth.route('/login')
def login():
    return "This is the login page"
