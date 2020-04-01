from flask import Flask, flash, redirect, render_template, request, session, Blueprint

from user_login.loginform import loginForm
from uabc_utilities.uabc_util import validate_user
# our custom utils file

from uabc_utilities.user import connection

from uabc_utilities.user import login_manager

log_me_in = Blueprint('login', __name__)




# TODO use flask login manager to utilize the login process and clean it up.
@log_me_in.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if validate_user(email, password):
            print(email + " " + " " + password)
            return render_template('dashboard.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)



