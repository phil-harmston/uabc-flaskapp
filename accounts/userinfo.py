class userinfo:

    def __init__(self, **kwargs):
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


