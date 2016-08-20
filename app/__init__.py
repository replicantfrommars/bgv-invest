from flask import Flask
from py2neo import ServiceRoot
import os

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['WTF_CSRF_ENABLED']=False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'

from views import *