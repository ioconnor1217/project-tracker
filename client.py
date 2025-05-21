# Import the Database class that contains all database interaction logic
from db import Database

# Define the Client class
class Client:

    @staticmethod
    def get_all():
        """
        Retrieve all clients from the database.
        Returns: list: A list of all clients, typically as dictionaries or tuples.
        """
        return Database.get_all_clients()

    @staticmethod
    def exists(name):
        """
        Check if a client with the given name already exists in the database.
        Args: name (str): The name of the client to check.
        Returns: bool: True if the client exists, False otherwise.
        """
        return Database.client_exists(name)

    @staticmethod
    def create(name):
        """
        Create a new client in the database with the given name.
        Args: name (str): The name of the client to create.
        Returns: int: The ID of the newly created client.
        """
        return Database.create_client(name)