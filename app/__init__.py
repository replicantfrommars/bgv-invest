from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import psycopg2

#Flask app config
app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY'] = 'super_secret_key'

#DB config
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'YKANALOSH',
    'password': '',
    'database': 'scrape'
}

#db connection
engine = create_engine(URL(**DATABASE)):

#import views.py
from app import views