# Import the Database class that handles all database interactions
from db import Database

# Define the Hours class
class Hours:
    @staticmethod
    def upsert_project_details(consultant_id, entries):
        """
        Insert or update project detail records for a consultant based on submitted entries.
        Args: consultant_id (int): ID of the consultant submitting the hours. entries (list): A list of dictionaries.
        Returns: tuple: (True, None) on success; (False, error_message) on failure.
        """
        for entry in entries:
            project_id = entry['project_id']
            client_id = entry['client_id']
            work_date = entry['date']
            description = entry['description']
            hours = entry['hours']

            # Get the linking record between the consultant and the project
            project_consultant_id = Database.get_project_consultant_id(consultant_id, project_id)
            if not project_consultant_id:
                # If no link exists, skip
                continue

            # Check if a work entry already exists for this date
            existing_detail_id = Database.find_project_detail(project_consultant_id, work_date)
            if existing_detail_id:
                # If it exists, update the record
                success = Database.update_project_detail(existing_detail_id, client_id, description, hours)
                if not success:
                    # Return failure if update fails
                    return False, "Failed to update project detail"
            else:
                # If it doesn't exist, insert a new record
                success = Database.insert_project_detail(project_consultant_id, client_id, work_date, description, hours)
                if not success:
                    # Return failure if insert fails
                    return False, "Failed to insert project detail"

        # Return success if processed successfully
        return True, None