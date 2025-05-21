# Import necessary libraries
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database class
class Database:

    @staticmethod
    def connect():
        # Check if we are connecting to Azure or local SQL Server
        is_azure = os.getenv("IS_AZURE", "False") == "True"

        try:
            if is_azure:
                # Connect to Azure SQL database
                conn = pyodbc.connect(
                    server=os.getenv("AZURE_DB_SERVER"),
                    database=os.getenv("AZURE_DB_NAME"),
                    user=os.getenv("AZURE_DB_USER"),
                    password=os.getenv("AZURE_DB_PASSWORD"),
                    encrypt="Yes",
                    trustservercertificate="No",
                    connection_timeout="30",
                    driver="{ODBC Driver 18 for SQL Server}"
                )
            else:
                # Connect to local SQL Server database
                conn = pyodbc.connect(
                    server=os.getenv("LOCAL_DB_SERVER"),
                    database=os.getenv("LOCAL_DB_NAME"),
                    user=os.getenv("LOCAL_DB_USER"),
                    password=os.getenv("LOCAL_DB_PASSWORD"),
                    trustservercertificate="Yes",
                    driver="{ODBC Driver 18 for SQL Server}"
                )
            return conn
        except Exception as e:
            # Print any connection error
            print("Database connection error:", e)
            return None

    @staticmethod
    def search_username(username):
        # Search for a username in the Login table
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
                # Return user info if found
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
        # Insert a new user into the Login table
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
        # Update a user's password
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Login SET Password = ? WHERE Login = ?", (new_password, username))
            conn.commit()
            return True
        except Exception as e:
            print("Error updating password:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def get_consultant_id_by_username(username):
        # Get ConsultantID based on username from joined Login and Consultant tables
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.ConsultantID 
                FROM Consultant c 
                JOIN Login l ON c.LoginID = l.LoginID 
                WHERE l.Login = ?
            ''', (username,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print("Error getting consultant ID:", e)
            return None
        finally:
            conn.close()


    @staticmethod
    def get_all_clients():
        # Retrieve all clients
        conn = Database.connect()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ClientID, ClientName FROM Client")
            return [{"id": row.ClientID, "name": row.ClientName} for row in cursor.fetchall()]
        except Exception as e:
            print("Error fetching clients:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def client_exists(name):
        # Check if a client with the given name already exists
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Client WHERE ClientName = ?", (name,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error checking client existence:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def create_client(name):
        # Create a new client and return the inserted ClientID
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Client (ClientName) OUTPUT INSERTED.ClientID VALUES (?)", (name,))
            row = cursor.fetchone()
            conn.commit()
            if row:
                return row.ClientID if hasattr(row, 'ClientID') else row[0]
            return None
        except Exception as e:
            print("Error creating client:", e)
            return None
        finally:
            conn.close()


    @staticmethod
    def get_all_projects():
        # Retrieve all projects
        conn = Database.connect()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ProjectID, ProjectName FROM Project")
            return [{"id": row.ProjectID, "name": row.ProjectName} for row in cursor.fetchall()]
        except Exception as e:
            print("Error fetching projects:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def project_exists(name):
        # Check if a project with the given name exists
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Project WHERE ProjectName = ?", (name,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error checking project existence:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def create_project(name):
        # Create a new project and return the inserted ProjectID
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Project (ProjectName) OUTPUT INSERTED.ProjectID VALUES (?)", (name,))
            row = cursor.fetchone()
            conn.commit()
            if row:
                return row.ProjectID if hasattr(row, 'ProjectID') else row[0]
            return None
        except Exception as e:
            print("Error creating project:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_project_consultant_id(consultant_id, project_id):
        # Retrieve the ProjectConsultantID that links a consultant to a project
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ProjectConsultantID
                FROM ProjectConsultant
                WHERE ConsultantID = ? AND ProjectID = ?
            ''', (consultant_id, project_id))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print("Error getting project consultant ID:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insert_project_detail(project_consultant_id, client_id, work_date, work_description, worked_hours):
        # Insert a new work entry into ProjectDetail table
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ProjectDetail (
                    ProjectConsultantID,
                    ClientID,
                    WorkDate,
                    WorkDescription,
                    WorkedHours
                ) VALUES (?, ?, ?, ?, ?)
            ''', (project_consultant_id, client_id, work_date, work_description, worked_hours))
            conn.commit()
            return True
        except Exception as e:
            print("Error inserting project detail:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def update_project_detail(project_detail_id, client_id, description, hours):
        # Update an existing work log entry in ProjectDetail
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ProjectDetail
                SET ClientID = ?, WorkDescription = ?, WorkedHours = ?, UpdatedDate = CURRENT_TIMESTAMP
                WHERE ProjectDetailID = ?
            ''', (client_id, description, hours, project_detail_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error updating project detail:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def find_project_detail(project_consultant_id, work_date):
        # Find a ProjectDetail record by consultant ID and work date
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ProjectDetailID FROM ProjectDetail
                WHERE ProjectConsultantID = ? AND WorkDate = ?
            ''', (project_consultant_id, work_date))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
        except Exception as e:
            print("Error finding project detail:", e)
            return None
        finally:
            conn.close()