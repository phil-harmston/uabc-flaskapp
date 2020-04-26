from flask import Flask, session
from uabc_util import connection
from uabc_util import verify_password
import secrets
from abcapp import app, db


# app = Flask(__name__, instance_path='/', static_url_path='/static')
# app.config.from_pyfile('instance/config.py')

    # print(mysql.connect_args)


# login_manager = LoginManager(app)




class User_info:


    def __init__(self, email, password):

        c, con = connection()
        self.email = email
        self.password = password

        # If the user exists get the full user.

        userinfosearch = "SELECT * FROM `uabc`.`UserAccounts` WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()

        if results == 1:
            columns = c.description

            templist = [{columns[index][0]: column for index, column in enumerate(value)} for value in results]


            # convert the list to dict
            full_user = templist[0]

            self.email = full_user['email']
            self.firstname = full_user['FirstName']
            self.lastname = full_user['LastName']
            self.address = full_user['Address']
            self.city = full_user['City']
            self.state = full_user['State']
            self.zipcode = full_user['ZipCode']
            self.phone = full_user['Phone']
            self.image = full_user['Image']
            self.sessionkey = full_user['UserSecret']







    def is_authenticated(self, email, password):
        userinfosearch = "SELECT UserEmail, UserPass, UserSecret FROM `uabc`.`UserAccounts` " \
                         "WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()



        if len(results) == 1:

            columns = c.description

            templist = [{columns[index][0]: column for index, column in enumerate(value)} for value in results]
            user_signin = templist[0]
            stored_pwd = user_signin['UserPass']

            print(user_signin)

            if verify_password(stored_pwd, password):
                """I need to assign a hash session ID, write it to the database and return the ID
                and set a cookie on the user computer with id"""
                secret = secrets.token_hex(20)
                print(secret)
                setsecret = "UPDATE `uabc`.`UserAccounts` SET UserSecret = '{secret}' WHERE UserEmail = '{email}';".format(email=email, secret=secret)
                c.execute(setsecret)
                con.commit()
                session['UserID'] = secret
                print(session['UserID'])
                return 1

        else:
            print('User not found')
            return 0


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)



