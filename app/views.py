from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore
from __init__ import app
from models import *

#views
@app.route('/')
@login_required
def home():
    return render_template('index.html')