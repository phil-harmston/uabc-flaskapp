from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_user, current_user, login_required
from User import User
from abcapp import app, bcrypt, db
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, PasswordField
from wtforms import validators, ValidationError
from uabc_util import connection
from sqlalchemy import update
from Store import Stores
your_store = Blueprint('your_store', __name__)



@your_store.route('/yourstore', methods=['GET', 'POST'])
@login_required
def yourstore():
    form = selectStore()
    store = "SELECT * FROM `uabc`.`Stores`;"
    c, con = connection()
    c.execute(store)
    store_list = c.fetchall()



    if current_user.is_authenticated:
        user = current_user
        id = user.id
    if request.method == 'POST':
        user_store = form.search_option.data

        mystore = store_list[int(user_store)][1]
        c, con = connection()

        #todo this is where I left off fix the comments below.  Trying to put in the store name into the users prefered store.

        update = "UPDATE `uabc`.`UserAccounts` SET UserStore='{user_store}' WHERE id={id};".format(user_store=mystore, id=id)

        c.execute(update)

        con.commit()


        return redirect(url_for('profile_dashboard.dashboard'))




def create_store_list(store_list):
    mylist = []
    for store in store_list:
        mylist.extend(i for i in store)

    return [(str(num), name) for num, name in enumerate(mylist)]


store = "SELECT STORE_NAME FROM `uabc`.`Stores`;"
c, con = connection()
c = con.cursor()
c.execute(store)

store_list = c.fetchall()
store_list = create_store_list(store_list)
print(store_list)
c.close()

class selectStore(FlaskForm):
    search_option = SelectField('Search by:', choices=store_list)





