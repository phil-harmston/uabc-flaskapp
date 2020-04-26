from flask import Flask, flash, redirect, render_template, request, session, Blueprint, url_for
from User import User
from flask_login import login_user, current_user, login_required, logout_user

user_logout = Blueprint('logout', __name__)

# TODO REWRITE THIS WHOLE PAGE TO ACCUALLY LOG THE USER OUT

@user_logout.route('/logout', methods=['GET','POST'])
@login_required
def logout():
        logout_user()
        return redirect(url_for('login.login'))



