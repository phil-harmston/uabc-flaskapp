from flask import Flask, flash, redirect, render_template, request, session, Blueprint
import os
import shutil
import hashlib
import binascii
from flaskext.mysql import MySQL
import generalforms

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from userinfo import userinfo

# import blueprint routes
from accounts.update_account import update_account
from user_login.login import log_me_in

# import custom utilities from our util files
from uabc_utilities.uabc_util import connection, soup_it


app = Flask(__name__, instance_path='/home/phil/python/abcapp', static_url_path='/static')
# sets up the app configuration from a file
app.config.from_pyfile('instance/config.py')

#register routes for our program
app.register_blueprint(update_account, url_prefix="/")
app.register_blueprint(log_me_in, url_prefix="/")

# connection to the database
# mysql = MySQL()
# mysql.init_app(app)
# con = mysql.connect()
# c = con.cursor()

#registers the updateaccount blueprint
# app.register_blueprint(mod)





@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = generalforms.searchCSCCode()
    if not session.get('logged_in'):
        return home()
    #get profile picture
    profile_pic = 'tux1.png'


    c, con = connection()
    # return a search on items from the hotlist table.
    hotlist_search = "select * FROM uabc.Inventory inner join uabc.HotList on Inventory.CS_CODE=HotList.CS_CODE where HotList.UserEmail = '{email}';".format(email=session['email'])
    c.execute(hotlist_search)

    # Use the column headers as the dictionary key on the search
    columns = c.description

    hotlist = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]

    if request.method == "GET":
        return render_template('dashboard.html', hotlist=hotlist, profile_pic=profile_pic, form=form)

    if request.method == "POST":
        sku = request.form['csc_val']


        # Start webdriver
        #----------------------------------------------------------------------
        # id of the Item CSC Code
        id = "ContentPlaceHolderBody_tbCscCode"

        # name of the Item Name box
        name = "ctl00$ContentPlaceHolderBody$tbCscCode"

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get("https://webapps2.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx")
        itemNameSearchBox = driver.find_element_by_name("ctl00$ContentPlaceHolderBody$tbItemName")








        itemIdSearchBox = driver.find_element_by_id(id)
        itemIdSearchBox.send_keys(sku)
        itemIdSearchBox.send_keys(Keys.ENTER)
        time.sleep(4)
        html = driver.page_source
        soup_it(html, sku, c)

        driver.close()
        # End Web driver
        # ----------------------------------------------------------------------


        inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME,  STATUS, CURRENT_PRICE FROM `uabc`.`Inventory` " \
            "WHERE CS_CODE = '{csc_val}';".format(csc_val=sku)
        c, con = connection()
        c = con.cursor()
        c.execute(inventorysearch)
        columns = c.description

        results = [{columns[index][0]:column for index, column in enumerate(value)} for value in c.fetchall()]
        c.close()
        #pprint.pprint(results)
        return render_template('dashboard.html', results=results, hotlist=hotlist, profile_pic=profile_pic, form=form)


    return render_template('dashboard.html', form=form)




@app.route('/hotlist', methods=['GET', 'POST'])
def hotlist():
    if request.method == "POST":
        cs_code = request.form['add_hotlist']
        #print(cs_code)
        UserEmail = session['email']
        #print(UserEmail)

        c, con = connection()

        insert = "INSERT INTO uabc.HotList(UserEmail, CS_CODE) "

        c.execute(insert + "VALUES( %s, %s)",
                  (UserEmail, cs_code))
        con.commit()

        return redirect('/dashboard')









@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "GET":
        cs_code = request.args
        cs_code = (cs_code['delete'])
        c, con = connection()

        remove = "DELETE FROM uabc.HotList WHERE CS_CODE = '{CS_CODE}';".format(CS_CODE=cs_code)

        c.execute(remove)
        con.commit()

        return redirect('/dashboard')


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    session['logged_in']=False
    return home()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = generalforms.loginForm()
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
            c,con =connection()
            c.execute(info + "VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (email, firstname, lastname, address, city, state, zipcode, phone, passwd))
            con.commit()
            con.close()
            # create a directory for our user
            usertree = '/home/phil/python/abcapp/users/{useremail}/profile/imgs'.format(useremail=email)
            os.makedirs(usertree)
            # copy default information to that directory
            defaultprofile = '/home/phil/python/abcapp/default_profile/'
            target = '/home/phil/python/abcapp/static/users/{useremail}/profile/'.format(useremail=email)
            src_files = os.listdir(defaultprofile)

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




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)