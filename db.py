import pyodbc
import bcrypt

class Database:
    @staticmethod
    def connect():
        """
        Establish a new database connection.
        """
        try:
            conn = pyodbc.connect(
                server="IANS-LAPTOP",
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
        """
        Searches for a username in the Login table.
        :param username: string
        :return: dict containing user details or None
        """
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
                    "HashedPassword": row[2].strip()
                }
            return None
        except Exception as e:
            print("Error while searching username:", e)
            return None

    @staticmethod
    def register_user(username, plain_password):
        """
        Hash the password and store it in the database.
        """
        hashed_password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode('utf-8')

        conn = Database.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO Login (Login, Password) VALUES (?, ?)"
            cursor.execute(sql, (username, hashed_password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error registering user:", e)
            return False

    @staticmethod
    def update_user_password(username, new_hashed_password):
        """
        Update a user's password in the database.
        :param username: string
        :param new_hashed_password: string (hashed password)
        :return: bool indicating success or failure
        """
        conn = Database.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            sql = "UPDATE Login SET Password = ? WHERE Login = ?"
            cursor.execute(sql, (new_hashed_password, username))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error updating password:", e)
            return False