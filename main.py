from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder="template")

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'test'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'baza'


# Intialize MySQL
mysql = MySQL(app)
@app.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin

    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('index.html', bla=session['loggedin'])
    else:
        return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    # Check if user is loggedin

    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('about.html', bla=session['loggedin'])
    else:
        return render_template('about.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    user=False
    print(session)
    print(session.keys())
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        print('FORMA: ', request.form)
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}' AND password = '{password}'")
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect('/')
        else:
            # Account doesnt exist or username/password incorrect
            return redirect('/login')
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)



# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
