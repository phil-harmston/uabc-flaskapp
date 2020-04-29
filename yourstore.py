from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, TextAreaField, SubmitField, RadioField, SelectField, StringField, PasswordField
from wtforms import validators, ValidationError
from uabc_util import connection

#function takes in a mysql response from fetchall() and returns a list of value and name that can be used in dropdown box.
def create_store_list(store_list):
    mylist = []
    for index in (store_list):
        for i in index:
            mylist.append(i)

    listlen = len(mylist)
    listcount  = []
    for i in range(0, listlen):
        listcount.append(str(i))

    store_list = list(zip(listcount, mylist))
    return(store_list)


store = "SELECT STORE_NAME FROM `uabc`.`Stores`;"
c, con = connection()
c = con.cursor()
c.execute(store)

columns = c.description
store_list = c.fetchall()

store_list = create_store_list(store_list)

c.close()

class yourStore(FlaskForm):
    search_option = SelectField('Search by:', choices = store_list)





