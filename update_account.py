from flask import render_template, session, Blueprint,flash, redirect, url_for
from uabc_util import connection
from flask_login import login_user, current_user, logout_user, login_required
from User import User
from accountform import accountForm

from abcapp import app, bcrypt, db


update_account = Blueprint('update_account', __name__)

@update_account.route('/updateaccount', methods=['GET', 'POST'])
@login_required
def updateaccount():
    if current_user.is_authenticated:
        user = current_user

    form = accountForm()

    userinfosearch = "SELECT * FROM `uabc`.`UserAccounts` " \
                     "WHERE UserEmail = '{email}';".format(email=current_user.UserEmail)
    c, con = connection()
    c.execute(userinfosearch)
    user = c.fetchall()
    print(user)


    con.close()


    return render_template('account.html', form=form)

    #return"This is the update account page"