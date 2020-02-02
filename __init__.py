from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import shutil
import random
import hashlib
import binascii
from flaskext.mysql import MySQL
from random import randint
import re
import generalforms
import pprint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bs
import re
from lxml import etree
import pandas as pd
import html5lib





app = Flask(__name__, instance_path='/home/phil/python/abcapp', static_url_path='/static')

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

def check_sql_string(sql, values):
    unique = "%PARAMETER%"
    sql = sql.replace("?", unique)
    for v in values: sql = sql.replace(unique, repr(v), 1)
    return sql

def soup_it(html, sku):
    soup = bs(html, 'lxml')
    infodict = {}

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblSku")
        infodict.update({'SKU': span.text})
    except AttributeError:
        pass

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblDesc")
        infodict.update({'Description': span.text})
    except AttributeError:
        pass

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblWhsInv")
        infodict.update({'Warehouse_Inventory': span.text})
    except AttributeError:
        pass

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblWhsOnOrder")
        infodict.update({'Warehouse_On_Order': span.text})
    except AttributeError:
        pass

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblStatus")
        infodict.update({'Status': span.text})
    except AttributeError:
        pass

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblPrice")
        infodict.update({'Price': span.text})
    except AttributeError:
        pass

    try:
        dfs = pd.read_html(html, header=0)
        for df in dfs:
            print(df)
    except ValueError as e:
        print('Error: ' + str(e))

    print(infodict)
    price = str(infodict.get('Price'))
    status = str(infodict.get('Status'))

    update_data = """UPDATE LIQUOR SET CURRENT_PRICE= ?, STATUS=? WHERE CS_CODE=?;"""
    values = (price, status, sku)
    print(check_sql_string(update_data, values))
        #cursor.execute(check_sql_string(update_data, values))
        #mydb.commit()

        #time.sleep(5)

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


@app.route('/updateaccount', methods=['GET', 'POST'])
def updateaccount():
    form = generalforms.accountForm()
    if not session.get('logged_in'):
        return home()
    if request.method == "GET":
        return render_template('account.html', form=form)

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

        return render_template('account.html', form=form)
    else:
        return render_template('createaccount.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return home()
    #get profile picture
    profile_pic = 'tux1.png'








    c, con = connection()
    hotlist_search = "select * FROM uabc.Inventory inner join uabc.HotList on Inventory.CS_CODE=HotList.CS_CODE where HotList.UserEmail = '{email}';".format(email=session['email'])
    c.execute(hotlist_search)
    columns = c.description

    hotlist = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]
    #print(hotlist)
    #print(session['email'])

    if request.method == "GET":
        return render_template('dashboard.html', hotlist=hotlist, profile_pic=profile_pic)

    if request.method == "POST":

        # Start webdriver
        #----------------------------------------------------------------------
        # id of the Item CSC Code
        id = "ContentPlaceHolderBody_tbCscCode"

        # name of the Item Name box
        name = "ctl00$ContentPlaceHolderBody$tbCscCode"
        # options = Options()
        # options.add_argument("--headless")
        #driver = webdriver.Chrome('/snap/bin/chromium.chromedriver')

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get("https://webapps2.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx")
        itemNameSearchBox = driver.find_element_by_name("ctl00$ContentPlaceHolderBody$tbItemName")

        # find the search box on the webpage

        #print(sku)









    # End Web driver
    #----------------------------------------------------------------------
        sku = request.form['csc_val']
        itemIdSearchBox = driver.find_element_by_id(id)
        itemIdSearchBox.send_keys(sku)
        itemIdSearchBox.send_keys(Keys.ENTER)
        html = driver.page_source
        soup_it(html, sku)
        time.sleep(5)
        driver.close()

        #print(searchval)

        inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME FROM `uabc`.`Inventory` " \
            "WHERE CS_CODE = '{csc_val}';".format(csc_val=sku)


        c, con = connection()

        c.execute(inventorysearch)
        columns = c.description

        results = [{columns[index][0]:column for index, column in enumerate(value)} for value in c.fetchall()]
        pprint.pprint(results)
        return render_template('dashboard.html', results=results, hotlist=hotlist, profile_pic=profile_pic)


    return render_template('dashboard.html')


@app.route('/hotlist', methods=['GET', 'POST'])
def hotlist():
    if request.method == "POST":
        cs_code = request.form['cs_code']
        UserEmail = session['email']

        c, con = connection()

        insert = "INSERT INTO uabc.HotList(UserEmail, CS_CODE) "

        c.execute(insert + "VALUES( %s, %s)",
                  (UserEmail, cs_code))
        con.commit()
        con.close()
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
        con.close()
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
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        userinfosearch = "SELECT UserEmail, firstname, UserPass FROM `uabc`.`UserAccounts` " \
                         "WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()
        print(results)
        if len(results) == 1:


            for r in results:
                thisemail = r[0]
                thisuser = r[1]
                stored_pwd = r[2]

            validpass = verify_password(stored_pwd, password)



            if validpass:
                session['logged_in'] = True
                session['username'] = thisuser
                session['email'] = thisemail
                return redirect('dashboard')
            else:
                error = "invalid username or password"
                return render_template('login.html', form=form, error=error)
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