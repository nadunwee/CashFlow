from flask import Flask, flash, redirect, render_template, request, session
from flask_mysqldb import MySQL
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
        return redirect("/dashbord")

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

@app.route("/dashbord", methods=["GET", "POST"])
def dashbord():
    if len(session) == 0:
        return redirect("/login")
    
    # Get the username
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT username FROM users WHERE id = %s', (session["user_id"],))
    result  = cursor.fetchone()
    # Remove () , and ' ' from result
    if result:
        username = result[0]
        username = username.strip("'")  # Remove single quotes

    # Get whole flow table
    cursor.execute('SELECT * FROM flow WHERE id = %s', (session["user_id"],))
    results  = cursor.fetchall()

    # Get the totoal income
    cursor.execute("SELECT SUM(amount) AS total_income FROM flow WHERE type = 'income' and id = %s", (session["user_id"],))
    income  = cursor.fetchone()
    total_income = float(income[0])

    # Get total expences
    cursor.execute("SELECT SUM(amount) AS total_expence FROM flow WHERE type = 'expence' and id = %s", (session["user_id"],))
    expence  = cursor.fetchone()
    total_expence = float(expence[0])

    # Get Balance
    balance = total_income - total_expence

    return render_template("dashbord.html", username=username, results=results, balance=balance)

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

        # Add to the database
        cursor.execute('INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s)', (username, name, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return render_template("login.html")

@app.route("/income", methods=["GET", "POST"])
def income():
    if len(session) == 0:
        return redirect("/login")
    
    if request.method == "GET":
        return render_template("income.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        method = request.form.get("income-method")
        amount = request.form.get("in-amount")
        type = request.form.get("income")
        user_id = session["user_id"]

        # Check if method or amount empty
        if not method or not amount:
            return apology("Blank Method or Amount")
        
        # Add to the database
        cursor.execute('INSERT INTO flow (method, amount, type, id) VALUES (%s, %s, %s, %s)', (method, amount, 'income', user_id))
        mysql.connection.commit()
        cursor.close()

        return redirect("/dashbord")

@app.route("/expence", methods=["GET", "POST"])
def expence():
    if len(session) == 0:
        return redirect("/login")
    
    if request.method == "GET":
        return render_template("expence.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        cursor = mysql.connection.cursor()

        method = request.form.get("expence-method")
        amount = request.form.get("ex-amount")
        user_id = session["user_id"]

        # Check if method or amount empty
        if not method or not amount:
            return apology("Blank Method or Amount")
        
        # Add to the database
        cursor.execute('INSERT INTO flow (method, amount, type, id) VALUES (%s, %s, %s, %s)', (method, amount, 'expence', user_id))
        mysql.connection.commit()
        cursor.close()

        return redirect("/expence")