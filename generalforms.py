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

class accountForm(FlaskForm):
    firstname = StringField('First Name', [validators.DataRequired('First Name')])
    lastname = StringField('Last Name', [validators.DataRequired('Last Name')])
    address = StringField('Address', [validators.DataRequired('Street Address')])
    city = StringField('City', [validators.DataRequired('City')])
    state = StringField('State', [validators.DataRequired('State')])
    zipcode = StringField('Zip Code', [validators.DataRequired('Zip Code')])
    email = StringField('Email', [validators.DataRequired('Email Address')])
    phone = StringField('Phone', [validators.DataRequired('Phone')])
    pass1 = StringField('Password', [validators.DataRequired('Password')])
    pass2 = StringField('Re-type Password', [validators.DataRequired('Re-Type Password')])
    submit = SubmitField("Send")
class searchForm(FlaskForm):
    csc_val = StringField('Search Items in Database', [validators.input_required('Search')])
    submit = SubmitField("SEARCH")

class loginForm(FlaskForm):
    email = StringField('User Email', [validators.DataRequired('Email Address')])
    password = StringField('password', [validators.DataRequired('Password')])