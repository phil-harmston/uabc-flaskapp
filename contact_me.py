#TODO REWRITE THIS WHOLE PAGE AS IT IS COMPLETELY WRONG

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = generalforms.contactform()
    if request.method == "POST":
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
            return render_template('contact.html', form=form)