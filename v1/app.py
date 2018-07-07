import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
#from utils import database
import urllib2, json

app = Flask(__name__)
#for sessions
app.secret_key = os.urandom(32)

#base
@app.route("/")
def start():
    return render_template('base.html', title = "Home", index = True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user already logged in, redirect to homepage
    if session.get('username'):
        flash("Whoops! You're already signed in.")
        return redirect(url_for('index'))

    # user entered login form
    elif request.form.get('login'):
        user = request.form.get('user')
        passw = request.form.get('passw')
        try:
            return database.authenticate(user,passw)
        except:
            flash("Whoops! You didn't fill out everything.")
            return render_template('login.html', login = False, passw = passw, user = user)

    # user didn't enter form
    else:
        return render_template('login.html', login = False)

#=======================FIX=======================================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if user already logged in, redirect to homepage(base.html)
    if session.get('username'):
        flash("Whoops! You're already signed in.")
        return redirect(url_for('index')) #something

    # user entered create account form
    elif request.form.get('signup'):
        user = request.form.get('user')
        passw1 = request.form.get('pass1')
        passw2 = request.form.get('pass2')
        return database.add_account(user,passw1,passw2)

    # user didn't enter form
    else:
        return render_template("signup.html", login = False)

#logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not session.get('username'):
        flash("Whoops! You're not logged in")
        return redirect(url_for('login'))
    else:
        flash("Yay! You've successfully logged out")
        session.pop('username')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.debug = True
    app.run(host = '0.0.0.0', port = 9002)
