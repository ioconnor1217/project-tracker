from flask import Flask, render_template, request, redirect, url_for, session, flash
from consultant import Consultant
from db import Database
import bcrypt

app = Flask(__name__)
app.secret_key = "xxx"  # Required for session management

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = Consultant.search_username(username)
        if user and Consultant.verify_password(password, user["HashedPassword"]):
            session["user"] = user["Username"]
            flash("Login successful!", "success")

            # Upgrade the password if necessary
            if not user["HashedPassword"].startswith("$2b$"):
                new_hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
                if Database.update_user_password(username, new_hashed_password):
                    print(f"Upgraded password for {username}")

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

@app.route('/favicon.ico')
def favicon():
    return "", 204 

if __name__ == "__main__":
    app.run(debug=True)