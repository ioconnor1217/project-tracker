from db import Database

class Consultant:
    def __init__(self, login_id, username, password):
        self.login_id = login_id
        self.username = username
        self.password = password

    @staticmethod
    def search_username(username):
        """
        Searches for a username in the Login table.
        """
        return Database.search_username(username)