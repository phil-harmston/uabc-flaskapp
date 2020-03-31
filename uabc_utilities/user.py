from uabc_utilities.uabc_util import connection


class userinfo:

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

    def is_active(self):
        pass

    def get_id(self):
        pass

    def is_authenticated(self):
        pass

    def is_anonymous(self):
        pass
