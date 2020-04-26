from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, StringField, PasswordField
from wtforms import validators, ValidationError

class loginForm(FlaskForm):
    email = StringField('User Email', [validators.InputRequired('Please enter your email address')])
    password = PasswordField('password', [validators.InputRequired('Password')])

