
from flask import render_template, request, Blueprint, flash, redirect, url_for
from accountform import accountForm
from flask.helpers import make_response
from abcapp import app, bcrypt, db
from User import User
from flask_login import login_user, current_user, logout_user, login_required
import random

create_account = Blueprint('create_account', __name__)

@create_account.route('/createaccount', methods=['GET','POST'])
def create():
    form = accountForm()
    # Form.validate_on_submit() ***MUST HAVE A csrf_token in the HTML FORM **WTF**
    if form.validate_on_submit():

        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        phone = form.phone.data
        passwd1 = form.pass1.data
        passwd2 = form.pass2.data



        if passwd1 == passwd2:
            hashed_pass = bcrypt.generate_password_hash(form.pass1.data).decode('utf-8')
            userID = random.randint(1, 1000000000)
            user = User(UserEmail=email, FirstName=firstname, LastName=lastname,
                        Address=address, City=city, State=state, ZipCode=zipcode, Phone=phone, UserPass=hashed_pass, UserID = userID)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("login.login"))
        else:
            print("passwords not equal")
            return render_template('createaccount.html', form=form)
    else:
        return render_template('createaccount.html', form=form)

