"""
This is the main page for the application
"""
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
import os
import re
import json
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)


@app.route("/")
def home():
    """
    The function that call that renders the home page
    """
    return render_template("home.html", date_time=datetime.now().strftime("%m-%d-%Y %H:%M"))


@app.route("/about")
def about():
    """
    The function that call that renders the about page
    """
    return render_template("about.html")


@app.route("/contact")
def contact():
    """
    The function that call that renders the about page
    """
    return render_template("contact.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        users = {}

        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
                print('1')
        except(FileNotFoundError):
            print('Error loading password storage.')
            flash('We ran into a issue on our end')
        if password != confirm_password:
            flash('Password does not match.')
            print('1.5')

        if is_registered(username):
            flash('Your account is already registered.')
            print('2.5')
            return redirect(url_for('login'))

        if not username:
            flash('Please enter your username.')
            print('3.5')

        if not password:
            flash('Please enter your password')
            print('4.5')

        if not is_complex(password):
            flash('Please enter a more complex password')
            flash(
                'Your password should have at least 8 characters and include lower and uppercase letters and numbers.')
            print('5.5')

        if (not is_registered(username)) and (is_complex(password)):
            encrypted_password = sha256_crypt.hash(password)
            users[username] = encrypted_password
            with open('users.json', 'w') as file:
                json.dump(users, file)
            flash('Your account was successfully created.')
            print('=> account created')
            return redirect(url_for('login'))
        else:
            print(f"=> error creating user {username}")
    return render_template('registration.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = {}

        # Checking if the users.json file exists and loading it
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                users = json.load(file)

        # Verifying if the user is registered
        if username in users:
            # Verifying the entered password with the stored hashed password
            if sha256_crypt.verify(password, users[username]):
                # Password matched, user logged in successfully
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('profile'))  # Redirect to the user's profile
            else:
                # Incorrect password
                flash('Invalid Password', 'danger')
                return render_template('login.html')
        else:
            # Username not found
            flash('Username not found', 'danger')
            return render_template('login.html')
    return render_template('login.html')


@app.route("/profile")
def profile():
    print('Here')
    if 'logged_in' in session and session['logged_in']:
        username = session.get('username', '')
        return render_template('profile.html', username=username)
    else:
        flash('Please login to view this page', 'danger')
        return redirect(url_for('login'))


def is_registered(username):
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)
            if username in users:
                return True
        return False


def is_complex(password):
    if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*()\-_+=<>!?[\]{}|\\]).{12,}$', password):
        return True
    return False


app.run(host='0.0.0.0', port=8081)

# if __name__ == '__main__':
#    app.run()



