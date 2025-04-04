import re
import bcrypt


def is_valid_email(email):
    """
    Checks if the email meets the RFC compliant pattern for email validation
    """
    email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.search(email_regex, email)
    if match:
        return True
    else:
        return False


def is_valid_password(password):
    """
    Checks if the password meets the minimum password requirements
    """
    min_length = 8
    requires_upper = True
    requires_lower = True
    requires_digit = True
    requires_special = True

    valid = is_min_length(password, min_length)
    if not valid:
        return valid, "Password must be at least {} characters long".format(min_length)

    if requires_upper:
        valid = contains_uppercase(password)
        if not valid:
            return valid, "Password must contain at least one uppercase letter."

    if requires_lower:
        valid = contains_lowercase(password)
        if not valid:
            return valid, "Password must contain at least one lowercase letter."

    if requires_digit:
        valid = contains_digit(password)
        if not valid:
            return valid, "Password must contain at least one number."

    if requires_special:
        valid = contains_special(password)
        if not valid:
            return valid, "Password must contain at least one special character."

    return True, None


def is_min_length(value, min_length):
    """
    Checks that the password/value meets minimum length requirements
    """
    if len(value) < min_length:
        return False
    return True


def contains_uppercase(password):
    """
    Checks if the passwork contains uppercase letters
    """
    if not any(char.isupper() for char in password):
        return False
    return True


def contains_lowercase(password):
    """
    Checks if the password contains lowercase letters
    """
    if not any(char.islower() for char in password):
        return False
    return True


def contains_digit(password):
    """
    Checks if the password contains digits
    """
    if not any(char.isdigit() for char in password):
        return False
    return True


def contains_special(password, special_chars="!@#$%^&*()_-=+[]{}\\|;:'\",<>./?"):
    """
    Checks if the password contains special characters
    """
    if not any(char in special_chars for char in password):
        return False
    return True


def is_valid_name(name):
    """
    Checks if the name is valid
    """
    pattern = r'^[a-zA-Z\d\s.\'-]+$'
    return bool(re.match(pattern, name))


def check_username(username):
    """
    Checks if the username is valid
    """
    if username == "":
        user_error = "Please enter a Username"
        return user_error
    if is_valid_name(username):
        return None
    else:
        user_error = "Usernames can only contain letters, numbers, spaces, apostrophes, periods, and hyphens"
        return user_error


def check_email(email):
    """
    Checks if the email is valid
    """
    if email == "":
        email_error = "Please enter your email address"
        return email_error
    elif is_valid_email(email):
        return None
    else:
        email_error = "Please enter a valid email address"
        return email_error


def check_password(password):
    """
    Checks if the password is valid
    """
    if password == "":
        pw_error = "Please enter your password"
        return pw_error
    valid, pw_error = is_valid_password(password)
    if valid:
        return None
    else:
        return pw_error


def hash_password(password):
    """
    Used to hash the password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_login_password(password, hashed_password):
    """
    Checks if the password entered matches the hashed password for the user
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))