from flask import Flask, flash, redirect, render_template, request, session, Blueprint
import os
import shutil
from accounts.accountform import accountForm

from uabc_utilities.uabc_util import connection, hash_password



create_account = Blueprint('create_account', __name__)

@create_account.route('/createaccount', methods=['GET','POST'])
def create():
    form = accountForm()
    if request.method == "POST":
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        phone = request.form['phone']
        passwd1 = request.form['pass1']
        passwd2 = request.form['pass2']

        if passwd1 == passwd2:
            passwd = passwd1
            passwd = hash_password(passwd)

            info = "INSERT INTO uabc.UserAccounts(UserEmail, FirstName, LastName, Address, City, State, ZipCode, Phone, UserPass) "
            c,con =connection()
            c.execute(info + "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (email, firstname, lastname, address, city, state, zipcode, phone, passwd))
            con.commit()
            con.close()
            try:
                # create a directory for our user
                usertree = '/home/phil/python/abcapp/users/{useremail}/profile/imgs'.format(useremail=email)
                os.makedirs(usertree)
                # copy default information to that directory
                defaultprofile = '/home/phil/python/abcapp/default_profile/'
                target = '/home/phil/python/abcapp/static/users/{useremail}/profile/'.format(useremail=email)
                src_files = os.listdir(defaultprofile)
            except:
                print("directory not created.")

            for file in src_files:
                full_file_name = os.path.join(defaultprofile, file)
                try:
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, target)
                except:
                    print('not copied ' + full_file_name)

            return redirect('login')
        else:

            return render_template('createaccount.html', form=form)

    if request.method == "GET":
        return render_template('createaccount.html', form=form)

