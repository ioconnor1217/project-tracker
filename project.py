from db import Database

class Project:
    @staticmethod
    def get_all():
        return Database.get_all_projects()

    @staticmethod
    def exists(name):
        return Database.project_exists(name)

    @staticmethod
    def create(name):
        return Database.create_project(name)
    
    @staticmethod
    def get_by_consultant(consultant_id):
        query = """
            SELECT p.ProjectID, p.Project
            FROM Project p
            JOIN ProjectConsultant pc ON p.ProjectID = pc.ProjectID
            WHERE pc.ConsultantID = ?
        """
        return Database.fetch_all(query, (consultant_id,))