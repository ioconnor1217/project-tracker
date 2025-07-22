# Import the Database class that handles all database interactions
from db import Database
from datetime import date, timedelta

# Define the Hours class
class Hours:
    @staticmethod
    def upsert_project_details(consultant_id, entries, deleted):
        rows_inserted = 0
        rows_updated = 0
        deleted_count = 0
        failed_entries = []

        # === Handle Deletions ===
        for entry in deleted:
            try:
                project_id = entry["project_id"]
                work_date = entry["date"]
                pc_id = Database.get_project_consultant_id(consultant_id, project_id)
                if pc_id:
                    detail_id = Database.find_project_detail(pc_id, work_date)
                    if detail_id:
                        deleted_successfully = Database.delete_project_detail(detail_id)
                        if deleted_successfully:
                            deleted_count += 1
            except Exception as e:
                print("Error deleting entry:", e)
                continue

        # === Handle Inserts and Updates ===

        for entry in entries:
            try:
                project_id = entry["project_id"]
                work_date = entry.get("date")
                work_description = entry.get("description", "")
                worked_hours = entry.get("hours", 0)

                pc_id = Database.get_project_consultant_id(consultant_id, project_id)
                if not pc_id:
                    print("Missing PC ID")
                    failed_entries.append(entry)
                    continue

                # Always insert a new record, allow multiple entries per project per day
                inserted = Database.insert_project_detail(
                    pc_id, work_date, work_description, worked_hours
                )
                if inserted:
                    rows_inserted += 1
                else:
                    failed_entries.append(entry)

            except Exception as e:
                print("Error inserting entry:", e)
                failed_entries.append(entry)
                continue

        return True, {
            "rows_inserted": rows_inserted,
            "rows_updated": rows_updated,
            "rows_deleted": deleted_count,
            "failed_entries": failed_entries
        }
    
    @staticmethod
    def get_logged_hours_by_month(consultant_id, year, month):
        print(f"Fetching hours for ConsultantID: {consultant_id}, Year: {year}, Month: {month}")
        return Database.get_monthly_logged_hours(consultant_id, year, month)

    @staticmethod
    def get_logged_hours_by_day(consultant_id, year, month, day):
        print(f"Fetching hours for ConsultantID: {consultant_id}, Year: {year}, Month: {month}, Day: {day}")
        conn = Database.connect()
        if not conn:
            print("Database connection failed.")
            return []
        try:
            cursor = conn.cursor()
            work_date = date(year, month, day)
            next_date = work_date + timedelta(days=1)
            print(f"[DEBUG] work_date value: {work_date}, next_date: {next_date}, type: {type(work_date)}")
            sql = '''
                SELECT 
                    c.Company AS client,
                    p.Project AS project,
                    pd.WorkDate AS date,
                    pd.WorkDescription AS description,
                    pd.WorkedHours AS hours,
                    pc.BillingRate AS rate
                FROM ProjectDetail pd
                JOIN ProjectConsultant pc ON pd.ProjectConsultantID = pc.ProjectConsultantID
                JOIN Project p ON pc.ProjectID = p.ProjectID
                JOIN Client c ON p.ClientID = c.ClientID
                WHERE pc.ConsultantID = ?
                AND pd.WorkDate >= ? AND pd.WorkDate < ?
                ORDER BY pd.WorkDate;
            '''
            cursor.execute(sql, (consultant_id, work_date, next_date))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            print(f"Day query rows returned: {len(result)}")
            return result
        except Exception as e:
            print("Error getting daily logged hours:", e)
            return []
        finally:
            conn.close()