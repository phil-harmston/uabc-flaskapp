from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField

from wtforms import validators, ValidationError
class contactform(FlaskForm):
    name = StringField("Name Of Student", [validators.DataRequired("Please enter your name.")])
    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    Address = TextAreaField("Address")
    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    Age = IntegerField("age")
    language = SelectField('Languages', choices=[('cpp', 'C++'),
                                                 ('py', 'Python')])
    submit = SubmitField("Send")