"""
Database initialization and connection management
SQLite database for Spring 2026 semester
"""

import sqlite3
import os


# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spring_2026.db")


def get_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def initialize_database():
    """Create database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create courses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            color TEXT,
            instructor TEXT
        )
    """)
    
    # Create assignments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            type TEXT,
            due_datetime TEXT NOT NULL,
            status TEXT DEFAULT 'Not Started',
            notes TEXT,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    """)

    # Create user settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

    # Initialize default settings
    from models.settings import Settings
    Settings.initialize_defaults()
