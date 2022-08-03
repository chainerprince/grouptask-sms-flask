from flask import Blueprint

auth = Blueprint('auth', __name__)

from smsapp.auth import routes