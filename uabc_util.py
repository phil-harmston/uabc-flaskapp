from flask import Flask, render_template
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
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
    c, con = connection()

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




def connection():
    app.config.from_pyfile('instance/config.py')
    mysql = MySQL(app)
    con = mysql.connect()
    c = con.cursor()
    # print(mysql.connect_args)

    return c, con




def web_driver(search_input):
    c, con = connection()
    # Start webdriver
    # ----------------------------------------------------------------------
    # id of the Item CSC Code
    id = "ContentPlaceHolderBody_tbCscCode"

    # name of the Item Name box
    name = "ctl00$ContentPlaceHolderBody$tbCscCode"

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://webapps2.abc.utah.gov/Production/OnlineInventoryQuery/IQ/InventoryQuery.aspx")
    try:
        itemNameSearchBox = driver.find_element_by_name("ctl00$ContentPlaceHolderBody$tbItemName")

        itemIdSearchBox = driver.find_element_by_id(id)
        itemIdSearchBox.send_keys(search_input)
        itemIdSearchBox.send_keys(Keys.ENTER)
        time.sleep(3)
        html = driver.page_source
        soup_it(html, search_input, c)
    except:
        pass
    driver.close()
    # End Web driver
    # ----------------------------------------------------------------------
