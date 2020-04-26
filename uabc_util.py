from flask import Flask, render_template
import os
import shutil
import hashlib
import binascii
from flaskext.mysql import MySQL
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

app = Flask(__name__)
app.config.from_pyfile('instance/config.py')





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

def soup_it(html, sku, c):
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
        print("No Status found")

    try:
        span = soup.find('span', id="ContentPlaceHolderBody_lblPrice")
        infodict.update({'Price': span.text})
    except AttributeError:
        print("No price found")

    try:
        dfs = pd.read_html(html, header=0)
        for df in dfs:
            records = df.to_dict('records')
            for r in records:
                recordStoreRecords(r, sku)
                print(r)
    except ValueError as e:
        print('Error: ' + str(e))


    price = str(infodict.get('Price'))
    status = str(infodict.get('Status'))

    c, con = connection()

    update_data = """UPDATE Inventory SET CURRENT_PRICE= ?, STATUS=? WHERE CS_CODE=?;"""
    values = (price, status, sku)
    #print(check_sql_string(update_data, values))
    c.execute(check_sql_string(update_data, values))
    con.commit()
    c.close()

def recordStoreRecords(r, sku):
    store_number = r['Store']
    store_number = "STORE_" + str(store_number)
    store_name = r['Name']
    quantity = r['Qty']
    store_address = r['Address']
    store_city = r['City']
    store_phone = r['Phone']

    c, con = connection()
    insert_data = "INSERT INTO Stores (STORE_ID, STORE_NAME ,ADDRESS, CITY, PHONE) VALUES ('{0}','{1}','{2}','{3}', '{4}')".format(store_number, store_name, store_address, store_city, store_phone)
    try:
        c.execute(insert_data)
        print(insert_data)
        con.commit()
    except:
        pass
    update_data = "UPDATE Inventory SET {0}={1} WHERE CS_CODE='{2}';".format(store_number, quantity, sku)
    try:
        c.execute(update_data)
        con.commit()
    except:
        pass
    c.close()


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
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
    app.config.from_pyfile('instance/config.py')
    mysql = MySQL(app)
    con = mysql.connect()
    c = con.cursor()
    # print(mysql.connect_args)

    return c, con




