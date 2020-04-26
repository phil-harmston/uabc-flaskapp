from flask import redirect, render_template, Blueprint, url_for
from abcapp import login_manager, app, db, bcrypt
from User import User
from flask_login import login_user, current_user, login_required
from loginform import loginForm



log_me_in = Blueprint('login', __name__)




# TODO use flask login manager to utilize the login process and clean it up.
@log_me_in.route('/login', methods=['GET', 'POST'])
@log_me_in.route('/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile_dashboard.dashboard'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(UserEmail=form.email.data).first()

        if user and bcrypt.check_password_hash(user.UserPass, form.password.data):
            login_user(user)
            return redirect(url_for('profile_dashboard.dashboard'))

    return render_template('login.html', form=form)
    # else:
    #     return render_template('login.html', form=form)
    



