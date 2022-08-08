from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField

class AddContactForm(FlaskForm):
    email = EmailField('Email')
    name = StringField('Name')
    message = TextAreaField('Message')
    