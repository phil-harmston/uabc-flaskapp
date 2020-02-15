def updateaccount():
    email = session['email']
    userinfosearch = "SELECT * FROM `uabc`.`UserAccounts` " \
                     "WHERE UserEmail = '{email}';".format(email=email)
    c, con = connection()
    c.execute(userinfosearch)

    columns = c.description
    # thisuser is a list of dictionaries
    thisuser = [{columns[index][0]: column for index, column in enumerate(value)} for value in c.fetchall()]
    # pulls the first item out becomes a dictionary
    thisuser = thisuser[0]

    userobj = userinfo(**thisuser)

    con.close()

    form = generalforms.accountForm(obj=userobj)
    if not session.get('logged_in'):
        return home()
    if request.method == "GET":




        return render_template('account.html', form=form)

    if request.method == "POST":
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        phone = request.form['phone']
        passwd1 = request.form['pass1']
        passwd2 = request.form['pass2']

        return render_template('account.html', form=form)
    else:
        return render_template('createaccount.html', form=form)