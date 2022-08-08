from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField


# Create Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username')
    email = EmailField('Email')
    password = PasswordField('Password')
    
    submit = SubmitField('Register')
    
# Create LoginForm
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    
    submit = SubmitField('Login')