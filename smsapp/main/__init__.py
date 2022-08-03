from flask import Blueprint

main = Blueprint('main', __name__)

from smsapp.main import routes