# Import the Database class that handles database interactions
from db import Database

# Define the Consultant class
class Consultant:

    @staticmethod
    def search_username(username):
        """
        Search for a consultant in the database by their username.
        Args: username (str): The username to search for.
        Returns: dict or None: A dictionary containing user data if found, or None if no match is found.
        """
        return Database.search_username(username)

    @staticmethod
    def get_consultant_id_by_username(username):
        """
        Retrieve the consultant's ID based on their username.
        Args: username (str): The username of the consultant.
        Returns: int or None: The consultant's ID if found, or None if not found.
        """
        return Database.get_consultant_id_by_username(username)