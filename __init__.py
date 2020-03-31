from flask import Flask, flash, redirect, render_template, request, session, Blueprint
import os
import shutil
import hashlib
import binascii
from flaskext.mysql import MySQL


# import loginManger
from flask_login import LoginManager, UserMixin

# import the webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from uabc_utilities import user

# import blueprint routes
from accounts.update_account import update_account
from user_login.login import log_me_in
from accounts.create_account import create_account
from dashboard.profile_dash import profile_dashboard
from dashboard.hotlist import my_hotlist
from user_login.logout import user_logout
from dashboard.delete import delete_record
from uabc_utilities import user
# import custom utilities from our util files
from uabc_utilities.uabc_util import connection, soup_it


app = Flask(__name__, instance_path='/home/phil/python/abcapp', static_url_path='/static')
# sets up the app configuration from a file
app.config.from_pyfile('instance/config.py')




#register routes for our program
app.register_blueprint(update_account, url_prefix="/")
app.register_blueprint(log_me_in, url_prefix="/")
app.register_blueprint(create_account, url_prefix="/")
app.register_blueprint(profile_dashboard, url_prefix="/")
app.register_blueprint(my_hotlist, url_prefix="/")
app.register_blueprint(user_logout, url_prefix="/")
app.register_blueprint(delete_record, url_prefix="/")




if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)