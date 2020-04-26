from abcapp import app, db, bcrypt, login_manager
from User import User
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, SubmitField, StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo




class accountForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=40)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=30)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=20)])
    zipcode = StringField('Zip Code', validators=[DataRequired(), Length(max=5)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=10)])
    pass1 = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])

    pass2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('pass1')])

    # recaptcha = RecaptchaField()

    def validate_email(self, email):
        user_exists = User.query.filter_by(UserEmail=email).first()
        if user_exists:
            raise ValidationError('That email has already been used.')

