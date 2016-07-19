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
    
class Margin(Form):
    pass 

class Register(Form):
    username = username = TextField('Username <br><i>(Case Sensitive)</i>', [validators.InputRequired(message=None)])
    password = PasswordField('Password <br><i>(Must be at least 8 characters with at least one letter and one number.)</i>:', [validators.InputRequired(message=None)])
    confirm_password = PasswordField('Confirm Password:', [validators.InputRequired(message=None)])

##### Route Decorators #####

    #////////////// Navigation /////////////////#

@app.route('/')
@app.route('/index')
def index():
    form = Login(request.form)
    return render_template('index.html', form=form)
    
@app.route('margin')
def margin():
    form = MarginCalulate(request.form) 
    billing_rate = form.billing_rate.data
    pay_rate = form.pay_rate.data 
    type = form.type.data
    client = form.client.data 
    VMS_fee = clients[client]  ####
    discount = clients[client] ####
    
    net_billing_rate = billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount)
    
    if type = "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]

    elif type = "Salary":
        loaded_cost = pay_rate * loaded_costs["W2"]
        
    elif type = "W2":
        loaded_cost = (pay_rate / 2080) * loaded_costs["Salary"]

    margin_dollars = net_billing_rate / loaded_cost
    margin_percent = margin_dollars / loaded_cost  
    
    return render_template('calculate_margin.html', form=form)

@app.route('needed_billing_rate')
def needed_billing_rate():

    form = BillingCalculate(request.form)

    pay_rate = form.pay_rate.data
    type = form.type.data
    target_margin = form.target_margin.data
    client = form.client.data 
    VMS_fee = clients[client]  ####
    discount = clients[client] ####
    total_discounts_and_fees = VMS_fee + discount
    
    
    if type = "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]
    
    elif type = "Salary":
        loaded_cost = pay_rate * loaded_costs["W2"]
    
    elif type = "W2":
        loaded_cost = (pay_rate / 2080) * loaded_costs["Salary"]
        
        
    if total_discounts_and_fees > 0: 
        billing_rate = loaded_cost / (1 - (target_margin + total_discounts_and_fees)) 
    
    elif total_discounts_and_fees < 0:
        billing_rate = loaded_cost / (1 - target_margin) 
    
    
    net_billing_rate = billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount)
    margin_dollars = net_billing_rate - loaded_cost
    

@app.route('pay_rate')
def pay_rate():

    form = RateCalculate(request.form)

    pay_rate = form.pay_rate.data
    type = form.type.data
    target_margin = form.target_margin.data
    client = form.client.data 
    VMS_fee = clients[client]  ####
    discount = clients[client] ####
    
    #net_billing_rate = billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount) 
    
    
    if type = "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]
    
    elif type = "Salary":
        loaded_cost = pay_rate * loaded_costs["W2"]
    
    elif type = "W2":
        loaded_cost = (pay_rate / 2080) * loaded_costs["Salary"]
        
    if type = "Salary":
        pay_rate = net_billing_rate * (1 - margin) / ((1 + rando(type)) * 2080)
    else:
        pay_rate = net_billing_rate * (1 - margin) / (1 + rando(type))
        
    margin_dollars = net_billing_rate - loaded_cost
    
    
    
def rando(type):
    if type = "IC":
        return .01
        
    elif type = "Salary":
        return .4
        
    elif type = "W2":
        return .2 
    

######## App Startup ###########

if __name__ == '__main__':
    loaded_costs = {"W2" : 1.2, "Salary" : 1.4, "IC" : 1.01}
	app.run()
