from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import hashlib
import binascii
from flaskext.mysql import MySQL
from random import randint
import re
import generalforms
import pprint
app = Flask(__name__, instance_path='/home/phil/python/abcapp')

app.config.from_pyfile('instance/config.py')

# connection to the database
mysql = MySQL()
mysql.init_app(app)
con = mysql.connect()
c = con.cursor()

def emailvalidation(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



def connection():
    #mysql = MySQL(app)

    con = mysql.connect()
    c = con.cursor()
    # print(mysql.connect_args)

    return c, con

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['logged_in']==False:
        return home()

    if request.method == "GET":
        return render_template('dashboard.html')

    print(session['logged_in'])
    if request.method == "POST":
        searchval = request.form['csc_val']
        print(searchval)

        inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME FROM `uabc`.`Inventory` " \
                              "WHERE CS_CODE = '{csc_val}';".format(csc_val=searchval)

        #print(inventorysearch)
        c, con = connection()

        c.execute(inventorysearch)
        columns = c.description
        #print(columns)
        results = [{columns[index][0]:column for index, column in enumerate(value)} for value in c.fetchall()]
        pprint.pprint(results)



    return render_template('dashboard.html')







@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return home()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = generalforms.loginForm()
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # hash the password


        # print(password)
        # print(email)
        userinfosearch = "SELECT UserEmail, firstname, UserPass FROM `uabc`.`UserAccounts` " \
                         "WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()

        if len(results) == 1:
            for r in results:
                thisuser = r[1]
                stored_pwd = r[2]

            validpass = verify_password(stored_pwd, password)
            print(r)


            if validpass:
                session['logged_in'] = True
                session['username'] = thisuser
                return render_template('dashboard.html')
            else:
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)

    else:
        return render_template('login.html', form=form)



@app.route('/createaccount', methods=['GET','POST'])
def create():
    form = generalforms.accountForm()
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

            c.execute(info + "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (email, firstname, lastname, address, city, state, zipcode, phone, passwd))
            con.commit()
            return render_template('login.html')
        else:

            return render_template('createaccount.html', form=form)

    if request.method == "GET":
        return render_template('createaccount.html', form=form)




@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = generalforms.contactform()
    if request.method == "POST":
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
            return render_template('contact.html', form=form)


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     form = accountForm(request.form)
#     if request.method == 'POST':
#         firstname = request.form['firstname']
#         print(firstname)
#
#     if form.validate():
#         # Save the comment here.
#         flash('Hello ' + name)
#     else:
#         flash('All the form fields are required. ')
#         return render_template('test.html', form=form)





if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)