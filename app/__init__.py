from flask import Flask
from py2neo import ServiceRoot
import os

# Create app
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['WTF_CSRF_ENABLED']=False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gwxkmmbzhvlitq:_IWTuiJFHAhJVsUYwmVJGdEN4q@ec2-54-227-245-222.compute-1.amazonaws.com:5432/damm4q15n6qaur'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login.html'

from views import *