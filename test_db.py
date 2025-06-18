import pyodbc
from datetime import date
from db import Database

def test_query():
    conn = Database.connect()
    cursor = conn.cursor()
    sql = '''
        SELECT 
            p.Project AS project,
            pd.WorkDate AS date,
            pd.WorkDescription AS description,
            pd.WorkedHours AS hours
        FROM ProjectDetail pd
        JOIN ProjectConsultant pc ON pd.ProjectConsultantID = pc.ProjectConsultantID
        JOIN Project p ON pc.ProjectID = p.ProjectID
        WHERE pc.ConsultantID = ?
        AND pd.WorkDate >= ?
        AND pd.WorkDate < ?
        ORDER BY pd.WorkDate;
    '''
    consultant_id = 2
    start_date = date(2025, 6, 1)
    end_date = date(2025, 7, 1)
    cursor.execute(sql, (consultant_id, start_date, end_date))
    rows = cursor.fetchall()
    print("Raw rows:", rows)
    conn.close()

if __name__ == "__main__":
    test_query()