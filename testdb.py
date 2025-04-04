import pyodbc
import bcrypt
import getpass

def connect_to_db():
    """
    Establish a connection to the database.
    """
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=IANS-LAPTOP;"
            "DATABASE=ProjectTracker;"
            "UID=sa;"
            "PWD=121792;"
            "TrustServerCertificate=Yes;"
        )
        return conn
    except Exception as e:
        print("❌ Database connection error:", e)
        return None

def fetch_users():
    """
    Retrieve and display a list of usernames and their hashed passwords from the Login table.
    Then prompt for expected plaintext passwords and verify.
    """
    conn = connect_to_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT Login, Password FROM Login")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("⚠️ No users found in the database.")
            return

        # Display the list of users and their hashed passwords
        print("\n🔍 Users retrieved from the database:\n")
        user_data = []
        for row in rows:
            username = row[0]
            hashed_password = row[1]
            user_data.append((username, hashed_password))
            print(f"👤 Username: {username} | Hashed Password: {hashed_password}")

        print("\nEnter expected plaintext passwords to verify matches...\n")

        # Prompt for expected passwords and verify them
        for username, hashed_password in user_data:
            expected_password = getpass.getpass(f"Enter expected password for {username}: ")

            if bcrypt.checkpw(expected_password.encode(), hashed_password.encode()):
                print(f"✅ Password match for {username}\n")
            else:
                print(f"❌ Incorrect password for {username}\n")

    except Exception as e:
        print("❌ Error fetching users:", e)

if __name__ == "__main__":
    fetch_users()