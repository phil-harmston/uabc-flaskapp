from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from user_login.loginform import loginForm

# our custom utils file
from uabc_utilities.uabc_util import connection, verify_password


log_me_in = Blueprint('login', __name__)

@log_me_in.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        userinfosearch = "SELECT UserEmail, firstname, UserPass FROM `uabc`.`UserAccounts` " \
                         "WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()
        if len(results) == 1:

            for r in results:
                thisemail = r[0]
                thisuser = r[1]
                stored_pwd = r[2]

            validpass = verify_password(stored_pwd, password)



            if validpass:
                session['logged_in'] = True
                session['name'] = thisuser
                session['email'] = thisemail
                return redirect('dashboard')

        else:
            flash("invalid username or password")
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)