# Import the Database class to access database functions
from db import Database

# Define the Project class
class Project:
    @staticmethod
    def get_all():
        """
        Retrieve a list of all projects from the database.
        Returns: list: A list of dictionaries representing all projects.
        """
        return Database.get_all_projects()

    @staticmethod
    def exists(name):
        """
        Check whether a project with the given name already exists.
        Args: name (str): The name of the project to check.
        Returns: bool: True if the project exists, False otherwise.
        """
        return Database.project_exists(name)

    @staticmethod
    def create(name):
        """
        Create a new project in the database with the specified name.
        Args: name (str): The name of the new project.
        Returns: int: The ID of the newly created project.
        """
        return Database.create_project(name)