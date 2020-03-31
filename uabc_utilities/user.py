from uabc_utilities.uabc_util import connection
from flask_login import LoginManager, UserMixin


c, con = connection()
class User(UserMixin):

    def __init__(self, **kwargs):
        self.user_id = kwargs['UserID']
        self.email = kwargs["UserEmail"]
        self.firstname = kwargs["FirstName"]
        self.lastname = kwargs["LastName"]
        self.address = kwargs["Address"]
        self.city = kwargs["City"]
        self.state = kwargs["State"]
        self.zipcode = kwargs["ZipCode"]
        self.phone = kwargs["Phone"]
        self.username = kwargs["UserName"]
        self.isadmin = kwargs["isAdmin"]
        self.userage = kwargs["UserAge"]
        self.birthday = kwargs["UserBirthday"]

    def user_email(self, email):
        userinfosearch = "SELECT UserEmail, firstname, UserPass FROM `uabc`.`UserAccounts` " \
                     "WHERE UserEmail = '{email}';".format(email=email)
        c, con = connection()
        c.execute(userinfosearch)
        results = c.fetchall()
        print(results)
        return results

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_id(int(user_id))

    def is_active(self):
        pass

    def get_id(user_id):
        idsearch = "SELECT * FROM `uabc`.`UserAccounts` " \
                         "WHERE UserID = '{user_id}';".format(UserID=user_id)
        c, con = connection()
        c.execute(idsearch)
        results = c.fetchall()
        print(results)
        return id

    def is_authenticated(self):
        pass

    def is_anonymous(self):
        pass
