from .models import User, get_todays_recent_posts
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)

@app_route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'];
        password = request.form['password'];

        if len(username) < 6:
            flash('Your username is shorter than 6 characters.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters')
        elif not User(username).register(password):
            flash('A user with that name already exists')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')