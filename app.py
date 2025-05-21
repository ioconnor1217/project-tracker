# Import necessary libraries
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

# Import business logic from custom modules
from consultant import Consultant
from project import Project
from client import Client
from hours import Hours

# Initialize Flask app
app = Flask(__name__)
# Set the secret key used for session management
app.secret_key = os.environ.get("SECRET_KEY", "dev_2")

# Route: Landing page (renders login page)
@app.route("/")
def index():
    return render_template("login.html")

# Route: Handles both GET and POST requests for login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get username and password from the form
        username = request.form["username"]
        password = request.form["password"]

        print(f"Attempting login for {username}")
        user = Consultant.search_username(username)

        if user:
            print(f"User found: {user}")
            # Check if the password matches
            if password == user["Password"].strip():
                session["user"] = user["Username"]  # Store username in session
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                print(f"Password mismatch for {username}")
        else:
            print(f"No user found for {username}")

        flash("Invalid username or password.", "danger")

    # For GET requests or failed logins, re-render the login page
    return render_template("login.html")

# Route: Handles API login requests via JSON
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Input validation
    if not username:
        return jsonify(success=False, errorMessage="Please enter your username")
    if not password:
        return jsonify(success=False, errorMessage="Please enter your password")

    user = Consultant.search_username(username)
    # Validate credentials
    if user and password == user["Password"].strip():
        session["user"] = user["Username"]
        return jsonify(success=True)
    elif user:
        return jsonify(success=False, errorMessage="Incorrect password")
    else:
        return jsonify(success=False, errorMessage="User not found")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# Route: Logs out the user by clearing the session
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Route: Prevents errors from favicon requests by returning empty response
@app.route('/favicon.ico')
def favicon():
    return "", 204

# Route: Simple health check (used by Azure or monitoring tools)
@app.route('/health')
def health():
    return 'OK', 200

# Route: Hours logging page (only accessible if logged in)
@app.route("/hours")
def log_hours():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("hours.html", user=session["user"])

# Route: Submits hours via AJAX (POST request with JSON)
@app.route('/submit_hours', methods=['POST'])
def submit_hours():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    # Get consultant ID from the logged-in user's username
    username = session['user']
    consultant_id = Hours.get_consultant_id_by_username(username)
    if not consultant_id:
        return jsonify({'status': 'error', 'message': 'Consultant not found'}), 400

    # Attempt to insert or update project detail records
    success, error = Hours.upsert_project_details(consultant_id, data)
    if success:
        return jsonify({'status': 'success', 'message': 'Hours saved successfully'})
    else:
        return jsonify({'status': 'error', 'message': error}), 500

# Route: Returns list of all projects in JSON format (for dropdowns)
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(Project.get_all())

# Route: Returns list of all clients in JSON format (for dropdowns)
@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify(Client.get_all())

# Route: Checks if a project with the given name already exists
@app.route('/api/check_project', methods=['POST'])
def check_project():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'exists': False})
    return jsonify({'exists': Project.exists(name)})

# Route: Creates a new project and returns its ID
@app.route('/api/create_project', methods=['POST'])
def create_project():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Project name required'}), 400
    project_id = Project.create(name)
    return jsonify({'id': project_id})

# Route: Checks if a client with the given name already exists
@app.route('/api/check_client', methods=['POST'])
def check_client():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'exists': False})
    return jsonify({'exists': Client.exists(name)})

# Route: Creates a new client and returns its ID
@app.route('/api/create_client', methods=['POST'])
def create_client():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Client name required'}), 400
    client_id = Client.create(name)
    return jsonify({'id': client_id})

# Entry point: Runs the Flask development server
if __name__ == "__main__":
    # Prevent server from running automatically on Azure
    if os.environ.get("IS_AZURE", "False").lower() != "true":
        print("Starting Flask app locally...")
        app.run(debug=True)