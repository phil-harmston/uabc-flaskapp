from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from uabc_utilities.uabc_util import connection
from accounts.updateform import accountForm
from userinfo import userinfo
update_account = Blueprint('update_account', __name__)

@update_account.route('/updateaccount', methods=['GET', 'POST'])
def updateaccount():

    email = session['email']
    userinfosearch = "SELECT * FROM `uabc`.`UserAccounts` " \
                     "WHERE UserEmail = '{email}';".format(email=email)
    c, con = connection()
    c.execute(userinfosearch)

    columns = c.description
    # thisuser is a list of dictionaries
    thisuser = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]
    # pulls the first item out becomes a dictionary
    thisuser = thisuser[0]

    userobj = userinfo(**thisuser)

    con.close()

    form = accountForm(obj=userobj)

    return render_template('account.html', form=form)

    #return"This is the update account page"