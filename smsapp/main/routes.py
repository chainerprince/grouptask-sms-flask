from flask import render_template
from smsapp.main import main

@main.route('/')
def home():
    return render_template('main/index.html')