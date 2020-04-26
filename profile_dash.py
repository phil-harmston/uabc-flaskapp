from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, login_required
from User import User
from searchform import searchCSCCode
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from uabc_util import connection, soup_it
import time

profile_dashboard = Blueprint('profile_dashboard', __name__)


@profile_dashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.is_authenticated:
        user = current_user

    form = searchCSCCode()

    c, con = connection()
    # return a search on items from the hotlist table.
    # TODO Fix line to meet pep8 standards.
    hotlist_search = "select * FROM uabc.Inventory inner join uabc.HotList on Inventory.CS_CODE=HotList.CS_CODE where HotList.UserEmail = '{email}';".format(email=current_user.UserEmail)
    c.execute(hotlist_search)

    # Use the column headers as the dictionary key on the search
    columns = c.description

    hotlist = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]

    if request.method == "GET":
        return render_template('dashboard.html', hotlist=hotlist, form=form)

    if request.method == "POST":
        sku = form.csc_val.data


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
        try:
            itemNameSearchBox = driver.find_element_by_name("ctl00$ContentPlaceHolderBody$tbItemName")


            itemIdSearchBox = driver.find_element_by_id(id)
            itemIdSearchBox.send_keys(sku)
            itemIdSearchBox.send_keys(Keys.ENTER)
            time.sleep(3)
            html = driver.page_source
            soup_it(html, sku, c)
        except:
            driver.close()
        # End Web driver
        # ----------------------------------------------------------------------


        inventorysearch = "SELECT CS_CODE, CON_SIZE, CASE_PACK, PRODUCT_NAME,  STATUS, CURRENT_PRICE FROM `uabc`.`Inventory` " \
            "WHERE CS_CODE = '{csc_val}';".format(csc_val=sku)
        c, con = connection()
        c = con.cursor()
        c.execute(inventorysearch)
        # This line returns a list of dictionaries from the database so the column header is the key data is the value
        columns = c.description
        results = [{columns[index][0]:column for index, column in enumerate(value)} for value in c.fetchall()]
        c.close()

        return render_template('dashboard.html', results=results, hotlist=hotlist, form=form)


    return render_template('dashboard.html', form=form, hotlist=hotlist)
