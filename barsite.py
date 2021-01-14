from flask_login import LoginManager
from flask import Flask, render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, TextField, PasswordField
import gc
import sys
import requests
import logging
import json
import datetime
import couchbase
import nacl.pwhash
import nacl.utils

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
couchbase.enable_logging()
cb_su = 'admin'
cb_pass = 'passw0rd'

app = Flask(__name__)
app.secret_key = 'sup3rS3cr3t'  # Change this!


lm = LoginManager()
lm.init_app(app)
@lm.user_loader
def load_user(user_id):
    return User.get(user_id)

def cb_reg_account_crypto():
    inpass = input("choose a secure password: ")
    password = bytes(inpass, 'utf-8')
    inpin = input("choose a pin with 8 to 10 numbers: ")
    pin = bytes(inpin, 'utf-8')
    pinhash = nacl.pwhash.argon2id.str(pin)
    passhash = nacl.pwhash.argon2id.str(password)
    #print(nacl.pwhash.argon2id.verify(hash,password))
    print(pinhash)
    print(passhash)
    return passhash

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            inuser = request.form['username']
            print(inuser)
            inpass = request.form['password']
            print(inpass)
        except NameError:
            inuser = None
            inpass = None
            error = 'Invalid Credentials. Please try again.'
    else:
        #1return redirect(url_for('home'))
        return render_template('login.html', error=error)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route("/logout")
def logout():
    return render_template("logout.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
