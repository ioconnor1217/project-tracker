
from flask import Flask

app = Flask(__name__)

print("APP STARTED - MINIMAL APP")

@app.route("/")
def index():
    print("INDEX ROUTE HIT - MINIMAL APP")
    return "Hello from minimal app!", 200

"""try:
    import pyodbc
    import os
    import traceback
    from dotenv import load_dotenv
    from datetime import date
except Exception as e:
    print("IMPORT ERROR:", e)
    raise

# app.py
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

from consultant import Consultant
from project import Project
from client import Client
from hours import Hours

app = Flask(__name__)
print("APP STARTED")
app.secret_key = os.environ.get("SECRET_KEY", "dev_2")

@app.route("/")
def index():
    print("INDEX ROUTE HIT")
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        print(f"Attempting login for {username}")
        user = Consultant.search_username(username)

        if user:
            print(f"User found: {user}")
            if password == user["Password"].strip():
                session["user"] = user["Username"]
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                print(f"Password mismatch for {username}")
        else:
            print(f"No user found for {username}")

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

@app.route("/view_hours")
def view_hours():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("view_hours.html", user=session["user"])

@app.route("/api/logged_hours", methods=["GET"])
def get_logged_hours():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        consultant_id = Consultant.get_consultant_id_by_username(session["user"])
        if not consultant_id:
            return jsonify({"error": "Consultant not found"}), 404

        year = request.args.get("year", type=int)
        month = request.args.get("month", type=int)

        if not year or not month:
            now = datetime.now()
            year = now.year
            month = now.month

        data = Hours.get_logged_hours_by_month(consultant_id, year, month)
        print("LOGGED HOURS RESULT:", data)  # <-- debugging line
        return jsonify({"data": data})

    except Exception as e:
        print("Error in /api/logged_hours:", e)
        return jsonify({"error": "An error occurred"}), 500

@app.route("/log_hours")
def log_hours():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("log_hours.html", user=session["user"])

@app.route('/submit_hours', methods=['POST'])
def submit_hours():
    if 'user' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

    try:
        data = request.get_json()
        print("Received data:", data)

        consultant_id = data.get("consultant_id")
        if not consultant_id:
            return jsonify({'status': 'error', 'message': 'Missing consultant ID'}), 400

        entries = data.get("entries")
        if not entries:
            return jsonify({'status': 'error', 'message': 'No entries provided'}), 400

        success, result = Hours.upsert_project_details(consultant_id, entries)

        if not success:
            return jsonify({'status': 'error', 'message': result}), 500

        failed_count = len(result.get("failed_entries", []))
        total_processed = result.get("rows_inserted", 0) + result.get("rows_updated", 0)

        if failed_count > 0:
            return jsonify({
                'status': 'partial_success',
                'message': f"{total_processed} entries saved, {failed_count} entries failed.",
                'failed_entries': result.get("failed_entries")
            }), 207

        if total_processed == 0:
            return jsonify({'status': 'warning', 'message': 'No new or updated entries were saved.'}), 200

        return jsonify({
            'status': 'success',
            'message': f'{result.get("rows_inserted", 0)} inserted, {result.get("rows_updated", 0)} updated.'
        }), 200

    except Exception as e:
        print("Submit error:", traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e),
            'trace': traceback.format_exc()
        }), 500
    
@app.route("/api/consultant_id", methods=["GET"])
def get_consultant_id():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    consultant_id = Consultant.get_consultant_id_by_username(session["user"])
    if not consultant_id:
        return jsonify({"error": "Consultant ID not found"}), 404

    return jsonify({"consultant_id": consultant_id})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    print("SESSION:", session)

    if 'user' not in session:
        print("No user in session.")
        return jsonify([])

    username = session['user']
    print(f"Fetching projects for user: {username}")
    
    consultant = Consultant.search_username(username)
    if not consultant:
        print("Consultant not found for that user.")
        return jsonify([])

    consultant_id = Consultant.get_consultant_id_by_username(username)
    if not consultant_id:
        print("Consultant ID not found for that user.")
        return jsonify([])

    raw_projects = Project.get_by_consultant(consultant_id)
    print("Raw projects data from DB:", raw_projects)

    # Format projects to return 'id' and 'name' as required by frontend
    projects = []
    for p in raw_projects:
        projects.append({
            "id": p["ProjectID"],
            "name": p["Project"]
        })

    print("Formatted projects for JSON:", projects)
    return jsonify(projects)

@app.route('/api/check_project', methods=['POST'])
def check_project():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'exists': False})
    return jsonify({'exists': Project.exists(name)})

@app.route('/api/check_client', methods=['POST'])
def check_client():
    name = request.json.get('name', '').strip()
    if not name:
        return jsonify({'exists': False})
    return jsonify({'exists': Client.exists(name)})

@app.route('/api/clients', methods=['GET'])
def api_get_clients():
    from db import Database
    clients = Database.get_all_clients()
    return jsonify(clients)

@app.route("/test_consultant_projects/<int:consultant_id>")
def test_consultant_projects(consultant_id):
    projects = Project.get_by_consultant(consultant_id)
    return jsonify(projects)

if __name__ == "__main__":
    print("IN MAIN BLOCK")
    if os.environ.get("IS_AZURE", "False").lower() != "true":
        print("Starting Flask app locally...")
        app.run(debug=True)"""