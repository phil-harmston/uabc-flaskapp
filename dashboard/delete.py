from flask import Flask, flash, redirect, render_template, request, session, Blueprint
delete_record = Blueprint('delete_record', __name__)

@delete_record.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "GET":
        cs_code = request.args
        cs_code = (cs_code['delete'])
        c, con = connection()

        remove = "DELETE FROM uabc.HotList WHERE CS_CODE = '{CS_CODE}';".format(CS_CODE=cs_code)

        c.execute(remove)
        con.commit()

        return redirect('/dashboard')