# Import the Database class that handles all database interactions
from db import Database

# Define the Hours class
class Hours:

    @staticmethod
    def get_logged_hours_by_month(consultant_id, year, month):
        return Database.get_monthly_logged_hours(consultant_id, year, month)

    @staticmethod
    def upsert_project_details(consultant_id, entries):
        rows_inserted = 0
        rows_updated = 0
        failed_entries = []

        for entry in entries:
            try:
                project_id = entry['project_id']
                work_date = entry['date']
                description = entry['description']
                hours = entry['hours']

                print(f"Processing entry: {entry}")

                project_consultant_id = Database.get_project_consultant_id(consultant_id, project_id)
                if not project_consultant_id:
                    msg = f"No ProjectConsultant link for consultant {consultant_id} and project {project_id}"
                    print(msg)
                    failed_entries.append({"entry": entry, "reason": msg})
                    continue

                existing_detail_id = Database.find_project_detail(project_consultant_id, work_date)
                if existing_detail_id:
                    print(f"Updating ProjectDetail ID {existing_detail_id}")
                    success = Database.update_project_detail(existing_detail_id, description, hours)
                    if success:
                        rows_updated += 1
                    else:
                        return False, "Failed to update project detail"
                else:
                    print(f"Inserting new ProjectDetail for PCID {project_consultant_id}")
                    success = Database.insert_project_detail(project_consultant_id, work_date, description, hours)
                    if success:
                        rows_inserted += 1
                    else:
                        return False, "Failed to insert project detail"

            except Exception as e:
                import traceback
                print("Error in upsert_project_details:", traceback.format_exc())
                return False, str(e)

        return True, {
            "rows_inserted": rows_inserted,
            "rows_updated": rows_updated,
            "failed_entries": failed_entries
        }