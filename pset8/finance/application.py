import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.debug = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

     # Get user's cash balance
    rows_users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

     # Get user's shares balance
    rows_transactions = db.execute("SELECT symbol, company,  SUM(shares) AS shares FROM transactions WHERE user_id = :user_id GROUP BY symbol,company HAVING SUM(shares) > 0", user_id=session["user_id"])
    shares_balance =[]
    total_balance = 0

    # Get current shares prices
    for line in rows_transactions:
        current_price = lookup(line["symbol"])
        total_balance += line["shares"] * current_price["price"]
        shares_balance.append ({
            "symbol": line["symbol"],
            "company": line["company"],
            "shares": line["shares"],
            "price": usd(current_price["price"]),
            "total_per_share": usd(line["shares"] * current_price["price"])
            })

    cash = rows_users[0]["cash"]

    return render_template("index.html", cash=usd(cash), shares_balance=shares_balance, total_balance = usd(total_balance + cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

       # Ensure symbol was submitted
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("missing symbol", 400)

        # Get quotation price
        dprice = lookup(symbol)

        # Ensure "lookup" turned price
        if not dprice:
            return apology("invalid symbol", 400)

        # Ensure, shares is positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Ensure shares is more then 0
        if int(shares) <= 0:
            return apology("shares is less then 0", 400)



        # Get user cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Get payment for shares
        cash_before = rows[0]["cash"]
        total_price = dprice["price"] * int(shares)

        if total_price > cash_before:
            return apology("not enough money", 400)

        # update user cash balance
        db.execute("UPDATE users SET cash = cash - :total_price WHERE id = :user_id",
                            user_id = session["user_id"],
                            total_price = total_price)
        # Update user shares balance
        db.execute("INSERT INTO transactions (user_id, operation_type, symbol, company, price, shares) VALUES (:user_id, :operation_type, :symbol, :company, :price, :shares)",
                            user_id = session["user_id"],
                            operation_type = "buy",
                            symbol = symbol.upper(),
                            company = dprice["name"],
                            price = dprice["price"],
                            shares = int(shares))

        flash("Bought!")

        return redirect(url_for("index"))
    else:

        return render_template("buy.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get form data
    username = request.args.get("username")

    # Ensure username is more then 1 symbol
    if len(username) < 1:
        return jsonify(False)

    # Query database for username
    rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)

    # Ensure username isn`t exists
    if len(rows) == 0:
        return jsonify(True)
    else:
        return jsonify(False)

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

     # Get user's transactions
    rows_transactions = db.execute("SELECT data, symbol, company, price, shares FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    transactions =[]

    # Get current shares prices
    for line in rows_transactions:

        transactions.append ({
            "data": line["data"],
            "symbol": line["symbol"],
            "company": line["company"],
            "price": usd(line["price"]),
            "shares": line["shares"]
            })

    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("missing symbol", 400)

        # Get quotation price
        dprice = lookup(request.form.get("symbol"))

        # Ensure "looup" turned price
        if not dprice:
            return apology("invalid symbol", 400)

        # Make string with share`s price
        text = 'A share of ' + dprice['name'] + ' (' + symbol + ') ' + 'costs ' + usd(dprice['price'])

        # show user share`s price
        return render_template("quoted.html",text=text)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("this username isn't available.Choose another username", 400)

        # Ensure password was confirm
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("confirm password", 400)

        id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get form data
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("missing symbol", 400)

        # Ensure, shares is positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        # Ensure shares is more then 0
        if int(shares) <= 0:
            return apology("shares is less then 0", 400)

        shares_number = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol HAVING SUM(shares) > 0",
            user_id = session["user_id"],
            symbol = symbol.upper())

        if int(shares) > shares_number[0]["shares"]:
            return apology("not enought shares", 400)


        # Get quotation price
        dprice = lookup(symbol)

        # Get user cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Get payment for shares
        cash_before = rows[0]["cash"]
        total_price = dprice["price"] * int(shares)

        # update user cash balance
        db.execute("UPDATE users SET cash = :cash + :total_price WHERE id = :user_id",
                            user_id = session["user_id"],
                            cash = cash_before,
                            total_price = total_price)

        # Update user shares balance
        db.execute("INSERT INTO transactions (user_id, operation_type, symbol, company, price, shares) VALUES (:user_id, :operation_type, :symbol, :company, :price, :shares)",
                            user_id = session["user_id"],
                            operation_type = "sell",
                            symbol = symbol.upper(),
                            company = dprice["name"],
                            price = dprice["price"],
                            shares = -int(shares))

        flash("Sold!")

        return redirect(url_for("index"))

    else:

        rows_transactions = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY symbol ASC",
            user_id = session["user_id"])

        return render_template("sell.html", shares = rows_transactions)


@app.route("/refill", methods=["GET", "POST"])
@login_required
def refill():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

     # Get form data
        amount = request.form.get("amount")

        # Ensure symbol was submitted
        if not amount:
            return apology("missing amount", 400)

        # Ensure amount was submitted
        if  int(amount) < 0:
            return apology("amount is less then 0", 400)

        # Get user cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash_before = rows[0]["cash"]
        cash_after = usd(cash_before + int(amount))


        # update user cash balance
        db.execute("UPDATE users SET cash = :cash + :amount WHERE id = :user_id",
                            user_id = session["user_id"],
                            cash = cash_before,
                            amount = amount)

        flash(F"Your account's overdrawn is " + str(cash_after))

        return render_template("refill.html")
    else:
        return render_template("refill.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

