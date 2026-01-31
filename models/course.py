"""
Course model and database operations
"""

from db.database import get_connection


class Course:
    """Represents a course in the Spring 2026 semester."""
    
    def __init__(self, id=None, name="", color="", instructor=""):
        self.id = id
        self.name = name
        self.color = color
        self.instructor = instructor
    
    @staticmethod
    def create(name, color="", instructor=""):
        """Create a new course in the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (name, color, instructor) VALUES (?, ?, ?)",
            (name, color, instructor)
        )
        conn.commit()
        course_id = cursor.lastrowid
        conn.close()
        return course_id
    
    @staticmethod
    def get_all():
        """Retrieve all courses from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        courses = []
        for row in rows:
            course = Course(
                id=row["id"],
                name=row["name"],
                color=row["color"],
                instructor=row["instructor"]
            )
            courses.append(course)
        return courses
    
    @staticmethod
    def get_by_id(course_id):
        """Retrieve a specific course by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Course(
                id=row["id"],
                name=row["name"],
                color=row["color"],
                instructor=row["instructor"]
            )
        return None
