from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# User model
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

# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            return redirect(url_for('index'))
        else:
            message = 'Invalid email/password. Please try again.'
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST':
        username = request.form['uid']
        password = request.form['pwd']
        email = request.form['email']
        Phonenumber = request.form['Phonenumber']
        Zipcode = request.form['Zipcode']
        Address = request.form['Address']
        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            message = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not username or not password or not email:
            message = 'Please fill out all the fields!'
        else:
            # Create new user
            new_user = User(username=username, password=password, email=email,
                            Phonenumber=Phonenumber, Zipcode=Zipcode, Address=Address)
            db.session.add(new_user)
            db.session.commit()
            message = 'You have successfully registered!'
    return render_template('signup.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
