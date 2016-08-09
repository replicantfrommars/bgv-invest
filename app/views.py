from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
from models import *

#views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('security/login.html')

@app.route('/users')
@login_required
def display_users():
    return render_template('display_users.html', main_btn=True)

@app.route('/map')
@login_required
def display():
    return render_template('display.html', main_btn=True)

@app.route('/logout')
@login_required
def logout():
    return "Logout"