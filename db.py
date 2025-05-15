import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
print("IS_AZURE value:", os.getenv("IS_AZURE"))

class Database:
    @staticmethod
    def connect():
        is_azure = os.getenv("IS_AZURE", "False") == "True"

        try:
            if is_azure:
                # Use Azure Database
                conn = pyodbc.connect(
                    server="tcp:project-tracker-server.database.windows.net,1433",
                    database="project-tracker-db",
                    user="ianoconnor1217",
                    password="Neverdie100",
                    encrypt="Yes",
                    trustservercertificate="No",
                    connection_timeout="30",
                    driver="{ODBC Driver 18 for SQL Server}"
                )
            else:
                # Use Local Database
                conn = pyodbc.connect(
                    server="localhost",
                    database="ProjectTracker",
                    user="sa",
                    password="121792",
                    trustservercertificate="Yes",
                    driver="{ODBC Driver 18 for SQL Server}"
                )
            
            return conn
        except Exception as e:
            print("Database connection error:", e)
            return None

    @staticmethod
    def search_username(username):
        conn = Database.connect()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            sql = "SELECT LoginID, Login, Password FROM Login WHERE Login = ?"
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "LoginID": row[0],
                    "Username": row[1],
                    "Password": row[2].strip()
                }
            return None
        except Exception as e:
            print("Error while searching username:", e)
            return None

    @staticmethod
    def register_user(username, password):
        conn = Database.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Login (Login, Password) VALUES (?, ?)"
            cursor.execute(sql, (username, password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error registering user:", e)
            return False

    @staticmethod
    def update_user_password(username, new_password):
        """
        Update a user's password in the database.
        :param username: string
        :param new_password: string
        :return: bool indicating success or failure
        """
        conn = Database.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = "UPDATE Login SET Password = ? WHERE Login = ?"
            cursor.execute(sql, (new_password, username))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error updating password:", e)
            return False