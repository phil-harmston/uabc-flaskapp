from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import login_user, current_user, login_required
from User import User

import random
import hashlib

# import custom utilities from our util files
from uabc_util import connection

my_hotlist = Blueprint('my_hotlist', __name__)

@my_hotlist.route('/hotlist', methods=['GET', 'POST'])
@login_required
def hotlist():
    if current_user.is_authenticated:
        user = current_user
    if request.method == "POST":

        cs_code = request.form['add_hotlist']
        randNumber = random.randint(0, 100000)

        keystring = str(current_user.UserEmail) + str(cs_code) + str(randNumber)
        key = hashlib.sha256(keystring.encode())
        keycode = key.hexdigest()

        c, con = connection()

        insert = "INSERT INTO uabc.HotList(UserEmail, CS_CODE, KEYCODE)VALUES('{email}','{cs_code}', '{key}')"\
            .format(email=current_user.UserEmail, cs_code=cs_code, key=keycode)

        c.execute(insert)

        con.commit()

        return redirect(url_for('profile_dashboard.dashboard'))

