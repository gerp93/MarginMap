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


##### Route Decorators #####

    #////////////// Navigation /////////////////#

@app.route('/')
@app.route('/index')
def index():
    form = Login(request.form)
    return render_template('index.html', form=form)


######## App Startup ###########

if __name__ == '__main__':
	app.run()
