from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, PasswordField
from wtforms import validators, ValidationError

class searchCSCCode(FlaskForm):
    csc_val = StringField('Search by CSC Number', [validators.input_required('Search')])
    submit = SubmitField("SEARCH")
