import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Password validation helpers ---
def is_valid_password(password):
    """
    min_length = 8
    requires_upper = True
    requires_lower = True
    requires_digit = True
    requires_special = True

    if not is_min_length(password, min_length):
        return False, f"Password must be at least {min_length} characters long"
    if requires_upper and not contains_uppercase(password):
        return False, "Password must contain at least one uppercase letter."
    if requires_lower and not contains_lowercase(password):
        return False, "Password must contain at least one lowercase letter."
    if requires_digit and not contains_digit(password):
        return False, "Password must contain at least one number."
    if requires_special and not contains_special(password):
        return False, "Password must contain at least one special character."
    """

    return True, None

def is_min_length(value, min_length):
    return len(value) >= min_length

def contains_uppercase(password):
    return any(char.isupper() for char in password)

def contains_lowercase(password):
    return any(char.islower() for char in password)

def contains_digit(password):
    return any(char.isdigit() for char in password)

def contains_special(password, special_chars="!@#$%^&*()_-=+[]{}\\|;:'\",<>./?"):
    return any(char in special_chars for char in password)

# --- Username validation helpers ---
def is_valid_name(name):
    pattern = r'^[a-zA-Z\d\s.\'-]+$'
    return bool(re.match(pattern, name))

def check_username(username):
    if username == "":
        return "Please enter a Username"
    if is_valid_name(username):
        return None
    return "Usernames can only contain letters, numbers, spaces, apostrophes, periods, and hyphens"

def check_password(password):
    if password == "":
        return "Please enter your password"
    valid, pw_error = is_valid_password(password)
    return None if valid else pw_error

# --- API Endpoint for login validation ---
@app.route('/api/validate-login', methods=['POST'])
def validate_login():
    data = request.json
    username_error = check_username(data['username'])
    if username_error:
        return jsonify(success=False, errorMessage=username_error)
    
    password_error = check_password(data['password'])
    if password_error:
        return jsonify(success=False, errorMessage=password_error)

    # If no errors, return success
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)