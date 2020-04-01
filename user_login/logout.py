from flask import Flask, flash, redirect, render_template, request, session, Blueprint

user_logout = Blueprint('logout', __name__)

# TODO REWRITE THIS WHOLE PAGE TO ACCUALLY LOG THE USER OUT

@user_logout.route('/logout', methods=['GET','POST'])
def logout():

        return "<h1> you are logged out</h1>"


