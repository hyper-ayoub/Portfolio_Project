from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    Phonenumber = db.Column(db.String(15), nullable=True)
    Zipcode = db.Column(db.String(10), nullable=True)
    Address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

