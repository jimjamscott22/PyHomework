"""
Assignment model and database operations
"""

from db.database import get_connection
from datetime import datetime


class Assignment:
    """Represents an assignment in the Spring 2026 semester."""
    
    def __init__(self, id=None, course_id=None, title="", type="", 
                 due_datetime=None, status="Not Started", notes=""):
        self.id = id
        self.course_id = course_id
        self.title = title
        self.type = type
        self.due_datetime = due_datetime
        self.status = status
        self.notes = notes
    
    @staticmethod
    def create(course_id, title, type, due_datetime, status="Not Started", notes=""):
        """Create a new assignment in the database."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Convert datetime to string for storage
        due_str = due_datetime.isoformat() if isinstance(due_datetime, datetime) else due_datetime
        
        cursor.execute(
            """INSERT INTO assignments 
               (course_id, title, type, due_datetime, status, notes) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (course_id, title, type, due_str, status, notes)
        )
        conn.commit()
        assignment_id = cursor.lastrowid
        conn.close()
        return assignment_id
    
    @staticmethod
    def get_all():
        """Retrieve all assignments from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM assignments ORDER BY due_datetime")
        rows = cursor.fetchall()
        conn.close()
        
        assignments = []
        for row in rows:
            assignment = Assignment(
                id=row["id"],
                course_id=row["course_id"],
                title=row["title"],
                type=row["type"],
                due_datetime=row["due_datetime"],
                status=row["status"],
                notes=row["notes"]
            )
            assignments.append(assignment)
        return assignments
    
    @staticmethod
    def update(assignment_id, course_id, title, type, due_datetime, status, notes):
        """Update an existing assignment."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Convert datetime to string for storage
        due_str = due_datetime.isoformat() if isinstance(due_datetime, datetime) else due_datetime
        
        cursor.execute(
            """UPDATE assignments 
               SET course_id=?, title=?, type=?, due_datetime=?, status=?, notes=?
               WHERE id=?""",
            (course_id, title, type, due_str, status, notes, assignment_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(assignment_id):
        """Delete an assignment from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assignments WHERE id=?", (assignment_id,))
        conn.commit()
        conn.close()
