from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from consultant import Consultant
from db import Database

app = Flask(__name__)
app.secret_key = "xxx"  # Required for session management

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = Consultant.search_username(username)
        if user and password == user["Password"].strip():
            session["user"] = user["Username"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify(success=False, errorMessage="Please enter your username")
    if not password:
        return jsonify(success=False, errorMessage="Please enter your password")

    user = Consultant.search_username(username)
    if user and password == user["Password"].strip():
        session["user"] = user["Username"]
        return jsonify(success=True)
    elif user:
        return jsonify(success=False, errorMessage="Incorrect password")
    else:
        return jsonify(success=False, errorMessage="User not found")

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
    return redirect(url_for("login"))

@app.route('/favicon.ico')
def favicon():
    return "", 204 

@app.route('/health')
def health():
    return 'OK', 200

@app.route("/hours")
def log_hours():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("hours.html", user=session["user"])

@app.route("/api/validate-login", methods=["POST"])
def api_validate_login():
    data = request.get_json()
    print("Received data:", data)  # Debugging line
    username = data.get("username")
    password = data.get("password")

    user = Consultant.search_username(username)
    if user and password == user["Password"]:
        return {"success": True}, 200
    else:
        return {"success": False, "errorMessage": "Invalid username or password."}, 400

"""
if __name__ == "__main__":
    app.run(debug=True)
"""