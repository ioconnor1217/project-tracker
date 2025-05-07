import pyodbc

class Database:
    @staticmethod
    def connect():
        try:
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