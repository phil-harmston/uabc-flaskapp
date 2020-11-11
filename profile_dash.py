from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, login_required
from User import User
from searchform import searchCSCCode
from yourstore import selectStore

from uabc_util import connection, soup_it, web_driver
import time

profile_dashboard = Blueprint('profile_dashboard', __name__)


@profile_dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.is_authenticated:
        user = current_user

    storesearch = selectStore()
    form = searchCSCCode()

    # connections
    c, con = connection()

    # return a search on items from the hotlist table.
    # TODO Fix line to meet pep8 standards.
    hotlist_search = "select * FROM uabc.Inventory inner join uabc.HotList on Inventory.CS_CODE=HotList.CS_CODE where HotList.UserEmail = '{email}';".format(email=current_user.UserEmail)
    c.execute(hotlist_search)

    # Use the column headers as the dictionary key on the search
    columns = c.description

    hotlist = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]

    if request.method == "POST":

        # inventory_search = "select * FROM uabc.Inventory where Inventory.'{}' = ;"
        # c.execute(hotlist_search)
        return render_template('dashboard.html', results=results, hotlist=hotlist, form=form, storesearch=storesearch)

    if request.method == "POST":
        search_input = form.csc_val.data
        search_by = int(form.search_option.data)

        if search_by == 1:
            web_driver(search_input)
            inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME,  STATUS, CURRENT_PRICE FROM `uabc`.`Inventory` " \
                              "WHERE CS_CODE = '{csc_val}';".format(csc_val=search_input)
            c, con = connection()
            c = con.cursor()
            c.execute(inventorysearch)
            # This line returns a list of dictionaries from the database so the column header is the key data is the value
            columns = c.description
            results = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]
            c.close()


        if search_by == 2:
            inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME,  STATUS, CURRENT_PRICE FROM `uabc`.`Inventory` " \
                              "WHERE PRODUCT_NAME LIKE '%{name}%';".format(name = search_input)
            c, con = connection()
            c = con.cursor()
            c.execute(inventorysearch)
            # This line returns a list of dictionaries from the database so the column header is the key data is the value
            columns = c.description
            results = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]
            c.close()





        return render_template('dashboard.html', results=results, hotlist=hotlist, form=form, storesearch=storesearch)


    return render_template('dashboard.html', form=form, hotlist=hotlist, storesearch=storesearch)


