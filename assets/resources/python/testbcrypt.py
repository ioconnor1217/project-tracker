import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Example usage:
plain_password = "dirtmcgirt"
hashed_password = hash_password(plain_password)
print("Hashed password:", hashed_password)