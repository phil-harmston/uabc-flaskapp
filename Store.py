from abcapp import app, db



class Stores(db.Model):
    super(db.Model)

    __tablename__ = "Stores"

    STORE_ID = db.Column(db.String(45), primary_key=True)
    STORE_NAME = db.Column(db.String(45))
    ADDRESS = db.Column(db.String(45))
    CITY = db.Column(db.String(45))
    PHONE = db.Column(db.String(45))




