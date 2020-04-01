from flask import Flask
from uabc_utilities.uabc_util import connection
from flask_login import LoginManager, UserMixin
from flask_login.utils import login_user
from flaskext.mysql import MySQL

app = Flask(__name__)



    # print(mysql.connect_args)

#create a login object
login_manager = LoginManager(app)




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

    '''I am using the UserMixin to provide the default implementations for
   is_authenticated
   is_active
   is_anonymous
   '''

    @login_manager.user_loader
    def load_user(user_id):
        print("user_loader " + user_id )
        return User.get_id(int(user_id))


    ''' get_id()
    This method must return a unicode that uniquely identifies this user, 
    and can be used to load the user from the user_loader callback. Note that this 
    must be a unicode - if the ID is natively an int or some other type, you will 
    need to convert it to unicode. '''

    def get_id(user_id):
        print("get_id " + user_id)
        return 10






