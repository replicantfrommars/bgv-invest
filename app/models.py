from __init__ import app
### dependencies for flask security ###
from flask_sqlalchemy import SQLAlchemy 
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.forms import LoginForm
### dependencies for neo4j ###
import os
from py2neo import ServiceRoot, Graph, authenticate

#db setup
db = SQLAlchemy(app)

###flask security User and Role models###
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

#create user
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='nonadmin', description='End user')
    db.session.commit()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

### neo4j ###
# connection for graphenedb
# set up authentication parameters
graphenedb_url = os.environ.get("GRAPHENEDB_URL", "http://localhost:7474/db/data")
graph = Graph(graphenedb_url+"/db/data")