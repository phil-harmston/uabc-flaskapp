from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, PasswordField
from wtforms import validators, ValidationError

Search_options = [('1', 'CSC CODE'),('2', 'NAME')]
class searchCSCCode(FlaskForm):
    csc_val = StringField('Search', [validators.input_required('Search')])
    search_option = SelectField('Search by:', choices = Search_options)
    submit = SubmitField("SEARCH")
