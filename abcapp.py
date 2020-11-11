from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__, instance_path='/home/phil/python/abcapp', static_url_path='/static')
# sets up the app configuration from a file
app.config.from_pyfile('instance/config.py')

# for this to work apt-get install python-mysqldb (Linux Ubuntu, ...)
# sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
# pip install mysqlclient
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


import os
import shutil
import hashlib
import binascii
from flaskext.mysql import MySQL


# import the webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys

# import various files
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


# import blueprint routes
from update_account import update_account
from login import log_me_in
from create_account import create_account
from profile_dash import profile_dashboard
from hotlist import my_hotlist
from logout import user_logout
from delete import delete_record
from yourstore import your_store


# import custom utilities from our util files
from uabc_util import connection, soup_it




app.register_blueprint(log_me_in)
app.register_blueprint(update_account, url_prefix="/")
app.register_blueprint(create_account, url_prefix="/")
app.register_blueprint(profile_dashboard, url_prefix="/")
app.register_blueprint(my_hotlist, url_prefix="/")
app.register_blueprint(user_logout, url_prefix="/")
app.register_blueprint(delete_record, url_prefix="/")
app.register_blueprint(your_store, url_prefix="/")





if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=5000)
