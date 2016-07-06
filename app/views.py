from flask import flash, render_template, session, redirect, url_for, request, escape
from .user import User
from app import app

@app.route('/')
@app.route('/index')
def index():
    if 'user' in session:
        flash ('Logged in as %s' % escape(session['user']))
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['pass']
        if not User(user).verify_password(passw):
            flash('Username/password combination not recognized')
        else:
            session['user']=user
            flash('Logged in.')
            return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return "Dashboard"