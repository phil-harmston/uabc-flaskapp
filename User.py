from abcapp import app, db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask, flash, redirect, render_template, request, session, Blueprint, url_for
from flask_login import login_user, current_user, login_required, logout_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL
def unauthorized_callback():            # In call back url we can specify where we want to
       return redirect(url_for('login.login'))

class User(db.Model, UserMixin):
    super(db.Model)

    __tablename__ = "UserAccounts"

    UserEmail = db.Column(db.String(45))
    FirstName = db.Column(db.String(45))
    LastName = db.Column(db.String(45))
    Address = db.Column(db.String(45))
    City = db.Column(db.String(45))
    State = db.Column(db.String(45))
    ZipCode = db.Column(db.String(45))
    Phone = db.Column(db.String(45))
    UserPass = db.Column(db.String(45))
    UserName = db.Column(db.String(45))
    UserAge = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key = True)

    def __init(self, email, password):

        self.UserEmail = email
        self.UserPass = password



