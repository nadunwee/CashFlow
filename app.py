from flask import Flask, flash, redirect, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology

# Configure application
app = Flask(__name__)

# Add Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cashflow'
 
mysql = MySQL(app)

# Create a secreat key for WTF
app.config['SECRET_KEY'] = "secretkey"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        rows = cursor.fetchone()

        # Ensure username exists
        if rows == None:
            return apology("invalid username", 403)

        # Ensure username exists and password is correct
        if not check_password_hash(rows[-1], request.form.get("password")):
            cursor.close()
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/home", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("conform-password")

        # Check if username or password is empty
        if not username or not password:
            return apology("Invalid Username or Password: Blank")
        
        # Check if the passwords match
        if password != confirm_password:
            return apology("Invalid Password: Passwords do not match")
        
        # Check if username already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            return apology("Invalid Username: Username already exists")
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        cursor.execute('INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s)', (username, name, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return render_template("login.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    name = None
    form = NamerForm()
    # Validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("form subitted successfully")
    return render_template("test.html", name=name, form=form)

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")