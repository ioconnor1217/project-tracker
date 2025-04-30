import bcrypt
from db import Database

class Consultant:
    def __init__(self, login_id, username, hashed_password):
        self.login_id = login_id
        self.username = username
        self.hashed_password = hashed_password

    @staticmethod
    def search_username(username):
        """
        Searches for a username in the Login table.
        """
        return Database.search_username(username)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verifies a plaintext password against a hashed password.
        """
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode("utf-8")
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())