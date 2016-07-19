############## Imports #################

from flask import Flask, render_template, redirect, request, url_for, g, session, flash, abort
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import decimal
import random
import locale
import psycopg2
import os
import urllib.parse
locale.setlocale(locale.LC_ALL, '')

############ Boilerplate ###################

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
Bootstrap(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


############ DB Table Models #############################

class User(db.Model):
    __tablename__ =  'user'
    id = db.Column('id', db.Integer, primary_key = True, autoincrement=1)
    username = db.Column('username', db.String(20), unique=True)
    password = db.Column('password', db.String(100))

    def __init__(self , username, password):
        #self.id = User.query.count() + 1
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)



db.create_all()


############## WTForms Classes #######################

class Login(Form):
    password = PasswordField('Password <br><i>(Case Sensitive)</i>:', [validators.InputRequired(message=None)])

############# Functions #################

def content_test(pw):
    print("pw", pw)
    pwl = []
    for character in pw:
        pwl.append(character)
    print("list:", pwl)

    letter = False
    for item in pwl:
        if item in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            letter = True
            break

    number = False
    for item in pwl:
        if item in ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']:
            number = True
            break


    if number == True and letter == True:
        return True
    else:
        return False

##### Back End Decorators #####

@app.before_request
def before_request():
    g.user = current_user
    #print(current_user.id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
##### Route Decorators #####

    #////////////// Navigation /////////////////#

@app.route('/')
@app.route('/index')
def index():
    form = Login(request.form)
    return render_template('index.html', form=form)

@app.route('/calculate_margin')
@login_required
def calculate_margin():
    return render_template('calculate_margin.html')

@app.route('/calculate_billing_rate')
@login_required
def calculate_billing_rate():
    return render_template('calculate_billing_rate.html')

@app.route('/calculate_pay_rate')
@login_required
def calculate_pay_rate():
    return render_template('calculate_pay_rate.html')

@app.route('/login', methods=['GET','POST'])
def login(*args):
    valid_registration=request.args.get('valid_registration')
    form = Login(request.form)
    if request.method == 'GET':
        if 'error' in locals():
            print(error)
            return render_template('login.html', error=error, form=form)
        error = False
        return render_template('login.html', form=form, valid_registration=valid_registration)
    username = "keyot"
    password = form.password.data
    print(User.query.filter_by(username=username).all())
    registered_user = User.query.filter_by(username=username).first()
    if registered_user.check_password(password) == False:
        print("here")
        flash('Password is invalid' , 'error')
        error = True
        return render_template('/login.html', error=error, form=form)

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('account'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
######## App Startup ###########

if __name__ == '__main__':
	app.run()
