### imports
from functools import wraps
from flask import render_template, request
from flask_security import auth_token_required, roles_required
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
import requests
import json
from models import *

### views ###
#home
@app.route('/')
@login_required
def home():
    return render_template('index.html')

#users
@app.route('/users', methods=['GET', 'POST'])
@roles_required('admin')
def display_users():
    #vars 
    email, password="", ""
    #if post
    if request.method == 'POST':
        for i in request.form:
            if i == 'delete':
                usr=User.query.filter_by(email=request.form[i]).first()
                user_datastore.delete_user(usr)
                db.session.commit()
            elif i == 'email':
                email=request.form[i]
            elif i == 'password':
                password=request.form[i]
    if email and password:
        user_datastore.create_user(email=email, password=password)
        db.session.commit()
    #retrieve user data for rendering
    user_collection = User.query.all();
    users=set();
    for i in user_collection:
        users.add(i.email)
    #return
    return render_template('display_users.html', main_btn=True, users=users)

#display investor map
@app.route('/map')
@login_required
def display():
    req_statement = '{"statements":[{"statement":"MATCH path = (n)-[r]->(m) RETURN path", "resultDataContents":["graph"]}]}'
    r = requests.post(graphenedb_url+'/db/data/transaction/commit', data=req_statement)
    return render_template('display.html', main_btn=True, json_p=r.content)

#allow upload to database
@app.route('/post', methods=['POST'])
@auth_token_required
def post():
    #status constant
    STATUS_POST="Success"
    try:
        #retrieve and format payload
        payload = request.get_json()['Upload']
        payload = payload.replace('[u"row', '').replace('"]', '')
        node_collection = payload.split('", u"row')
        for row in node_collection:
            #format rows and prepare queries 
            row=row.split("nn_comp")
            n1, n2=row[0], row[1]
            n2 = n2.split("end_comp")
            n2, n3 = n2[0], n2[1]
            try:
                queries=["MERGE "+ n1, "MERGE "+ n3, "Match" + n1+","+n3+" MERGE (cat)-[rel1:has]->"+n2+"<-[rel2:has]-(city)"]
                for q in queries:
                    graph.cypher.execute(q)
            except SyntaxError as e:
                STATUS_POST="An error occurred while processing the upload: "+e.message
                print e
        return STATUS_POST
    except Exception as e:
        print "Error processing upload: "+e.message
        return "Error processing upload: "+e.message

#logout
@app.route('/logout')
@login_required
def logout():
    return "Logout"