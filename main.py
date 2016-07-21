############## Imports #################
from flask import Flask, render_template, redirect, request, url_for, g, session, flash, abort
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, PasswordField, validators, FloatField, SelectField
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
import decimal
import random
import locale
import psycopg2
import os
import decimal
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
    password = PasswordField('Password <br><i>(Case Sensitive)</i>:', [validators.InputRequired(message=None)])

class MarginCalculate(Form):
    client = SelectField(u'Client:', choices=[('Cetera Financial', 'Cetera Financial'), ('DiTech', 'DiTech'), ('Fairview', 'Fairview'), ('Farm Bureau', 'Farm Bureau'), ('Guide One', 'Guide One'),('Hy-Vee', 'Hy-Vee'),('Integrated Behavior Health Network', 'Integrated Behavior Health Network'),('Lifespace Communities', 'Lifespace Communities'),('Lifetouch', 'Lifetouch'), ('Merrill', 'Merrill'), ('MoneyGram', 'MoneyGram'), ('Nationstar', 'Nationstar'), ('Pioneer', 'Pioneer'), ('Hybrid', 'Hybrid'), ('Prime', 'Prime'), ('Principal Financial', 'Principal Financial'), ('Securian', 'Securian'), ('State of Iowa', 'State of Iowa'), ('State of Minnesota', 'State of Minnesota'), ('Unity Point Wellmark', 'Unity Point Wellmark'), ('Wells Fargo', 'Wells Fargo')])
    billingRate = FloatField('Billing Rate:', [validators.InputRequired(message=None)], default=55.00)
    payRate = FloatField('Pay Rate:', [validators.InputRequired(message=None)], default=58000)
    payType = SelectField(u'Pay Type:', choices=[('Salary','Salary'), ('W2', 'W2'), ('IC', 'IC')], default="Salary")

class BillingCalculate(Form):
    client = SelectField(u'Client:', choices=[('Cetera Financial', 'Cetera Financial'), ('DiTech', 'DiTech'), ('Fairview', 'Fairview'), ('Farm Bureau', 'Farm Bureau'), ('Guide One', 'Guide One'),('Hy-Vee', 'Hy-Vee'),('Integrated Behavior Health Network', 'Integrated Behavior Health Network'),('Lifespace Communities', 'Lifespace Communities'),('Lifetouch', 'Lifetouch'), ('Merrill', 'Merrill'), ('MoneyGram', 'MoneyGram'), ('Nationstar', 'Nationstar'), ('Pioneer', 'Pioneer'), ('Hybrid', 'Hybrid'), ('Prime', 'Prime'), ('Principal Financial', 'Principal Financial'), ('Securian', 'Securian'), ('State of Iowa', 'State of Iowa'), ('State of Minnesota', 'State of Minnesota'), ('Unity Point Wellmark', 'Unity Point Wellmark'), ('Wells Fargo', 'Wells Fargo')])
    targetMargin = FloatField('Target Margin:', [validators.InputRequired(message=None)], default=26.86)
    payRate = FloatField('Pay Rate:', [validators.InputRequired(message=None)], default=58000)
    payType = SelectField(u'Pay Type:', choices=[('Salary','Salary'), ('W2', 'W2'), ('IC', 'IC')], default="Salary")

class PayCalculate(Form):
    client = SelectField(u'Client:', choices=[('Cetera Financial', 'Cetera Financial'), ('DiTech', 'DiTech'), ('Fairview', 'Fairview'), ('Farm Bureau', 'Farm Bureau'), ('Guide One', 'Guide One'),('Hy-Vee', 'Hy-Vee'),('Integrated Behavior Health Network', 'Integrated Behavior Health Network'),('Lifespace Communities', 'Lifespace Communities'),('Lifetouch', 'Lifetouch'), ('Merrill', 'Merrill'), ('MoneyGram', 'MoneyGram'), ('Nationstar', 'Nationstar'), ('Pioneer', 'Pioneer'), ('Hybrid', 'Hybrid'), ('Prime', 'Prime'), ('Principal Financial', 'Principal Financial'), ('Securian', 'Securian'), ('State of Iowa', 'State of Iowa'), ('State of Minnesota', 'State of Minnesota'), ('Unity Point Wellmark', 'Unity Point Wellmark'), ('Wells Fargo', 'Wells Fargo')])
    billingRate = FloatField('Billing Rate:', [validators.InputRequired(message=None)], default=55.00)
    margin = FloatField('Target Margin:', [validators.InputRequired(message=None)], default=26.86)
    payType = SelectField(u'Pay Type:', choices=[('Salary','Salary'), ('W2', 'W2'), ('IC', 'IC')], default="Salary")

##### Back End Decorators #####
@app.before_request
def before_request():
    g.user = current_user
    #print(current_user.id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    
##### Helper Functions ######


def return_loaded_costs():
    
    return {"W2" : 1.2, "Salary" : 1.4, "IC" : 1.01}
 
    
def return_clients():       
             
    return {
        'Cetera Financial' : {'VMS_fee' : 0, 'discount' : 0 },
        'DiTech' : {'VMS_fee' : .03, 'discount' : 0 },
        'Fairview' : {'VMS_fee' : .03, 'discount' : 0 },
        'Farm Bureau' : {'VMS_fee' : 0, 'discount' : 0 },
        'Guide One' : {'VMS_fee' : 0, 'discount' : 0 },
        'Hy-Vee' : {'VMS_fee' : 0, 'discount' : 0 },
        'Integrated Behavior Health Network' : {'VMS_fee' : 0, 'discount' : 0 },
        'Lifespace Communities' : {'VMS_fee' : 0, 'discount' : 0 },
        'Lifetouch' : {'VMS_fee' : 0, 'discount' : 0 },
        'Merrill' : {'VMS_fee' : 0, 'discount' : 0 },
        'MoneyGram' : {'VMS_fee' : 0, 'discount' : 0 },
        'Nationstar' : {'VMS_fee' : .0295, 'discount' : 0 },
        'Pioneer Hybrid' : {'VMS_fee' : 0, 'discount' : 0 },
        'Prime' : {'VMS_fee' : 0, 'discount' : .03 },
        'Principal Financial' : {'VMS_fee' : 0, 'discount' : 0 },
        'Securian' : {'VMS_fee' : 0, 'discount' : 0 },
        'State of Iowa' : {'VMS_fee' : 0, 'discount' : .01 },
        'State of Minnesota' : {'VMS_fee' : 0, 'discount' : .01 },
        'Unity Point' : {'VMS_fee' : 0, 'discount' : 0 },
        'Wellmark' : {'VMS_fee' : 0, 'discount' : 0 },
        'Wells Fargo' : {'VMS_fee' : .02, 'discount' : 0 }
        
        }    
    
    
##### Route Decorators #####

#////////////// Navigation /////////////////#

@app.route('/')
@app.route('/index')
def index():
    form = Login(request.form)
    return render_template('index.html', form=form)

def rando(type):
    if type == "IC":
        return .01

    elif type == "Salary":
        return .4

    elif type == "W2":
        return .2

@app.route('/calculate_margin', methods=['GET','POST'])
@login_required
def calculate_margin():

    form = MarginCalculate(request.form)

    if request.method == 'GET':
        return render_template('calculate_margin.html', form=form)


    billing_rate = form.billingRate.data
    pay_rate = form.payRate.data
    type = form.payType.data
    client = form.client.data
    print(form.client.data)
    clients = return_clients()
    loaded_costs = return_loaded_costs()

    VMS_fee = clients[client]['VMS_fee']  ####
    discount = clients[client]['discount'] ####

    net_billing_rate = billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount)

    if type == "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]

    elif type == "W2":
        loaded_cost = pay_rate * loaded_costs["W2"]

    elif type == "Salary":
        loaded_cost = round((pay_rate / 2080) * loaded_costs["Salary"], 2)

    margin_dollars = round(net_billing_rate - loaded_cost, 2)
    margin_percent = round((margin_dollars / net_billing_rate) * 100, 2)

    return render_template('calculate_margin.html', form=form, margin_dollars=margin_dollars, margin_percent=margin_percent, net_billing_rate=net_billing_rate, loaded_cost=loaded_cost)

@app.route('/calculate_billing_rate', methods=['GET','POST'])
@login_required
def calculate_billing_rate():


    form = BillingCalculate(request.form)

    if request.method == 'GET':
        return render_template('calculate_billing_rate.html', form=form)


    pay_rate = form.payRate.data
    type = form.payType.data
    target_margin = form.targetMargin.data / 100
    client = form.client.data
    VMS_fee = clients[client]['VMS_fee']  ####
    discount = clients[client]['discount'] ####
    total_discounts_and_fees = VMS_fee + discount
    clients = return_clients()
    loaded_costs = return_loaded_costs()


    if type == "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]

    elif type == "W2":
        loaded_cost = pay_rate * loaded_costs["W2"]


    elif type == "Salary":
        loaded_cost = (pay_rate / 2080) * loaded_costs["Salary"]

    loaded_cost = round(loaded_cost, 2)


    if total_discounts_and_fees > 0:
        billing_rate = loaded_cost / (1 - (target_margin + total_discounts_and_fees))

    else:
        billing_rate = loaded_cost / (1 - target_margin)

    billing_rate = round(billing_rate, 2)


    net_billing_rate = round(billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount), 2)
    margin_dollars = round(net_billing_rate - loaded_cost, 2)

    return render_template('calculate_billing_rate.html', form=form, margin_dollars=margin_dollars, net_billing_rate=net_billing_rate, billing_rate=billing_rate, loaded_cost=loaded_cost)

@app.route('/calculate_pay_rate', methods=['GET','POST'])
@login_required
def calculate_pay_rate():

    form = PayCalculate(request.form)

    if request.method == 'GET':
        return render_template('calculate_pay_rate.html', form=form)


    billing_rate = form.billingRate.data
    type = form.payType.data
    margin = form.margin.data / 100
    client = form.client.data
    VMS_fee = clients[client]['VMS_fee']  ####
    discount = clients[client]['discount'] ####
    clients = return_clients()
    loaded_costs = return_loaded_costs()


    net_billing_rate = billing_rate - (billing_rate * VMS_fee) - (billing_rate * discount)


    if type == "Salary":
        pay_rate = (net_billing_rate * (1 - margin) / ((1 + rando(type)))) * 2080
    else:
        pay_rate = net_billing_rate * (1 - margin) / (1 + rando(type))

    pay_rate = round(pay_rate, 2)


    if type == "IC":
        loaded_cost = pay_rate * loaded_costs["IC"]


    elif type == "W2":
        loaded_cost = pay_rate * loaded_costs["W2"]

    elif type == "Salary":
        loaded_cost = pay_rate / 2080 * loaded_costs["Salary"]

    loaded_cost =  round(loaded_cost, 2)

    margin_dollars = round(net_billing_rate - loaded_cost, 2)

    return render_template('calculate_pay_rate.html', form=form, margin_dollars=margin_dollars, pay_rate=pay_rate, loaded_cost=loaded_cost, net_billing_rate=net_billing_rate)

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
    if registered_user is None:
        print("here")
        flash('Password is invalid' , 'error')
        error = True
        return render_template('/login.html', error=error, form=form)

    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

######## App Startup ###########
if __name__ == '__main__':

    #loaded_costs = {"W2" : 1.2, "Salary" : 1.4, "IC" : 1.01}


    """

    clients = {
    'Cetera Financial' : {'VMS_fee' : 0, 'discount' : 0 },
    'DiTech' : {'VMS_fee' : .03, 'discount' : 0 },
    'Fairview' : {'VMS_fee' : .03, 'discount' : 0 },
    'Farm Bureau' : {'VMS_fee' : 0, 'discount' : 0 },
    'Guide One' : {'VMS_fee' : 0, 'discount' : 0 },
    'Hy-Vee' : {'VMS_fee' : 0, 'discount' : 0 },
    'Integrated Behavior Health Network' : {'VMS_fee' : 0, 'discount' : 0 },
    'Lifespace Communities' : {'VMS_fee' : 0, 'discount' : 0 },
    'Lifetouch' : {'VMS_fee' : 0, 'discount' : 0 },
    'Merrill' : {'VMS_fee' : 0, 'discount' : 0 },
    'MoneyGram' : {'VMS_fee' : 0, 'discount' : 0 },
    'Nationstar' : {'VMS_fee' : .0295, 'discount' : 0 },
    'Pioneer Hybrid' : {'VMS_fee' : 0, 'discount' : 0 },
    'Prime' : {'VMS_fee' : 0, 'discount' : .03 },
    'Principal Financial' : {'VMS_fee' : 0, 'discount' : 0 },
    'Securian' : {'VMS_fee' : 0, 'discount' : 0 },
    'State of Iowa' : {'VMS_fee' : 0, 'discount' : .01 },
    'State of Minnesota' : {'VMS_fee' : 0, 'discount' : .01 },
    'Unity Point' : {'VMS_fee' : 0, 'discount' : 0 },
    'Wellmark' : {'VMS_fee' : 0, 'discount' : 0 },
    'Wells Fargo' : {'VMS_fee' : .02, 'discount' : 0 }

    }
    """
    app.run()
