import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class Database:

    @staticmethod
    def connect():
        is_azure = os.getenv("IS_AZURE", "False") == "True"

        try:
            if is_azure:
                conn_str = (
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    f"SERVER={os.getenv('AZURE_DB_SERVER')};"
                    f"DATABASE={os.getenv('AZURE_DB_NAME')};"
                    f"UID={os.getenv('AZURE_DB_USER')};"
                    f"PWD={os.getenv('AZURE_DB_PASSWORD')};"
                    f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
                )
            else:
                conn_str = (
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    f"SERVER={os.getenv('LOCAL_DB_SERVER')};"
                    f"DATABASE={os.getenv('LOCAL_DB_NAME')};"
                    f"UID={os.getenv('LOCAL_DB_USER')};"
                    f"PWD={os.getenv('LOCAL_DB_PASSWORD')};"
                    f"TrustServerCertificate=yes;"
                )
            return pyodbc.connect(conn_str)
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
            cursor.execute("SELECT LoginID, Login, Password FROM Login WHERE Login = ?", (username,))
            row = cursor.fetchone()
            if row:
                return {
                    "LoginID": row[0],
                    "Username": row[1],
                    "Password": row[2].strip()
                }
        except Exception as e:
            print("Error searching username:", e)
        finally:
            conn.close()
        return None

    @staticmethod
    def register_user(username, password):
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Login (Login, Password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except Exception as e:
            print("Error registering user:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def update_user_password(username, new_password):
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
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error getting consultant ID:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all_clients():
        conn = Database.connect()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ClientID, Company FROM Client")
            return [{"id": row.ClientID, "name": row.Company} for row in cursor.fetchall()]
        except Exception as e:
            print("Error fetching clients:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def client_exists(name):
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Client WHERE Company = ?", (name,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error checking client existence:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all_projects():
        conn = Database.connect()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ProjectID, Project FROM Project")
            return [{"id": row.ProjectID, "name": row.Project} for row in cursor.fetchall()]
        except Exception as e:
            print("Error fetching projects:", e)
            return []
        finally:
            conn.close()

    @staticmethod
    def project_exists(name):
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Project WHERE Project = ?", (name,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error checking project existence:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def get_project_consultant_id(consultant_id, project_id):
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
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error getting project consultant ID:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def insert_project_detail(project_consultant_id, work_date, work_description, worked_hours):
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            print(f"INSERTING: {project_consultant_id}, {work_date}, {work_description}, {worked_hours}")
            cursor.execute('''
                INSERT INTO ProjectDetail (ProjectConsultantID, WorkDate, WorkDescription, WorkedHours)
                VALUES (?, ?, ?, ?)
            ''', (project_consultant_id, work_date, work_description, worked_hours))
            conn.commit()
            return True
        except Exception as e:
            print("Error inserting project detail:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def update_project_detail(project_detail_id, description, hours):
        conn = Database.connect()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE ProjectDetail
                SET WorkDescription = ?, WorkedHours = ?, UpdatedDate = CURRENT_TIMESTAMP
                WHERE ProjectDetailID = ?
            ''', (description, hours, project_detail_id))
            conn.commit()
            return True
        except Exception as e:
            print("Error updating project detail:", e)
            return False
        finally:
            conn.close()

    @staticmethod
    def find_project_detail(project_consultant_id, work_date):
        conn = Database.connect()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ProjectDetailID
                FROM ProjectDetail
                WHERE ProjectConsultantID = ? AND WorkDate = ?
            ''', (project_consultant_id, work_date))
            row = cursor.fetchone()
            return row[0] if row else None
        except Exception as e:
            print("Error finding project detail:", e)
            return None
        finally:
            conn.close()

    @staticmethod
    def fetch_all(query, params=None):
        conn = Database.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print("Error in fetch_all:", e)
            return []
        finally:
            conn.close()