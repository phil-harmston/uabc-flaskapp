from flask import Flask, flash, redirect, render_template, request, session, Blueprint
from flask_login import login_user, current_user, login_required
from User import User
from uabc_util import connection
delete_record = Blueprint('delete_record', __name__)

@delete_record.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if current_user.is_authenticated:
        user = current_user
    if request.method == "GET":
        codes = request.args
        cs_code = codes['delete']

        c, con = connection()
        find_record = "select * from uabc.HotList where CS_CODE = '{cs_code}' and UserEmail = '{email}';"\
            .format(cs_code=cs_code, email= current_user.UserEmail)
        c.execute(find_record)

        columns = c.description

        record_for_removal = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]

        record_for_removal = record_for_removal[0]
        keycode = record_for_removal['KEYCODE']


        remove = "DELETE FROM uabc.HotList WHERE KEYCODE = '{keycode}';".format(keycode=keycode)

        c.execute(remove)
        con.commit()

        return redirect('/dashboard')

