from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, PasswordField
from wtforms import validators, ValidationError

class accountForm(FlaskForm):
    firstname = StringField('First Name', [validators.DataRequired('First Name')])
    lastname = StringField('Last Name', [validators.DataRequired('Last Name')])
    address = StringField('Address', [validators.DataRequired('Street Address')])
    city = StringField('City', [validators.DataRequired('City')])
    state = StringField('State', [validators.DataRequired('State')])
    zipcode = StringField('Zip Code', [validators.DataRequired('Zip Code')])
    email = StringField('Email', [validators.DataRequired('Email Address')])
    phone = StringField('Phone', [validators.DataRequired('Phone')])
    pass1 = PasswordField('Password', [validators.DataRequired('Password'),
                                       validators.length(min=8, message='Must be longer than eight characters')])
    pass2 = PasswordField('Re-type Password', [validators.DataRequired('Re-Type Password'),
                                               validators.length(min=8,
                                                      message='Must be longer than eight characters')])

    recaptcha = RecaptchaField()
    submit = SubmitField("Send")


