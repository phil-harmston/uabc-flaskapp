from flask import Flask, flash, redirect, render_template, request, session, Blueprint


# import custom utilities from our util files
from uabc_utilities.uabc_util import connection

my_hotlist = Blueprint('my_hotlist', __name__)

@my_hotlist.route('/hotlist', methods=['GET', 'POST'])
def hotlist():
    if request.method == "POST":
        cs_code = request.form['add_hotlist']
        #print(cs_code)
        UserEmail = session['email']
        #print(UserEmail)

        c, con = connection()

        insert = "INSERT INTO uabc.HotList(UserEmail, CS_CODE) "

        c.execute(insert + "VALUES( %s, %s)",
                  (UserEmail, cs_code))
        con.commit()

        return redirect('/dashboard')