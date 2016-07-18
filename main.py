############## Imports #################

from flask import Flask, render_template, redirect, request, url_for, g, session, flash, abort 
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
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

db.create_all() 

############## WTForms Classes #######################
	
    
class Login(Form):
    username = TextField('Username <br><i>(Case Sensitive)</i>:', [validators.InputRequired(message=None)])
    password = PasswordField('Password <br><i>(Case Sensitive)</i>:', [validators.InputRequired(message=None)])
    
class Register(Form):
    username = username = TextField('Username <br><i>(Case Sensitive)</i>', [validators.InputRequired(message=None)])
    password = PasswordField('Password <br><i>(Must be at least 8 characters with at least one letter and one number.)</i>:', [validators.InputRequired(message=None)])
    confirm_password = PasswordField('Confirm Password:', [validators.InputRequired(message=None)])
    
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
@login_required
def index():
    form = Login(request.form)
    return render_template('login.html', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')
    
    
    #////////////// User Management /////////////////#
	
@app.route('/register' , methods=['GET','POST'])
def register():
    form = Register(request.form)
    valid_registration = request.args.get('valid_registration')
    if request.method == 'GET':
        return render_template('register.html', form=form, valid_registration=valid_registration)
        
        
    users = db.session.query(User).all()
    user_check = []
    for user in users:
        user_check.append(user.username) 
    print(user_check)
    print('username:', form.username.data) 

    if form.username.data in user_check:
        valid_registration = "exists"
        return redirect(url_for('register', valid_registration=valid_registration))
        
        
    if form.password.data != form.confirm_password.data:
        valid_registration = "password_match" 
        return redirect(url_for('register', valid_registration=valid_registration))
        
    
    if content_test(form.password.data) is False:
           valid_registration = "password_content"
           return redirect(url_for('register', valid_registration=valid_registration))
           
    if len(form.password.data) < 8:
        valid_registration = "password_length"
        return redirect(url_for('register', valid_registration=valid_registration))
        
    if len(form.username.data) == 0:
        valid_registration = "empty"
        return redirect(url_for('register', valid_registration=valid_registration))
        
        
    user = User(form.username.data, form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    valid_registration = True

    return redirect(url_for('login', valid_registration=valid_registration))


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
    username = form.username.data
    password = form.password.data
    print(User.query.filter_by(username=username, password=password).all())
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        print("here")
        flash('Username or Password is invalid' , 'error')
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