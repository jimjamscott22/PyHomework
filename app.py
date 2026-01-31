"""
PyHomework - Main application window and navigation
Manages the root Tkinter window and view switching
"""

import tkinter as tk
from tkinter import ttk
from db.database import initialize_database
from ui.dashboard import DashboardFrame
from ui.course_form import CourseFormFrame
from ui.assignment_form import AssignmentFormFrame


class PyHomeworkApp:
    """Main application class that manages the Tkinter window and navigation."""
    
    def __init__(self):
        """Initialize the application window and setup."""
        self.root = tk.Tk()
        self.root.title("PyHomework - Spring 2026 Assignment Tracker")
        self.root.geometry("900x700")
        
        # Initialize database on startup
        initialize_database()
        
        # Container for all frames
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Navigation bar
        self.create_navigation()
        
        # Content area where frames will be displayed
        self.content_frame = tk.Frame(self.container, bg="white")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Dictionary to store frame instances
        self.frames = {}
        
        # Show dashboard by default
        self.show_frame("dashboard")
    
    def create_navigation(self):
        """Create the navigation bar with buttons to switch between views."""
        nav_frame = tk.Frame(self.container, bg="#2c3e50", height=50)
        nav_frame.pack(fill="x", side="top")
        
        # Navigation buttons
        btn_dashboard = tk.Button(
            nav_frame, 
            text="Dashboard", 
            command=lambda: self.show_frame("dashboard"),
            bg="#34495e",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=10,
            relief="flat"
        )
        btn_dashboard.pack(side="left", padx=5, pady=5)
        
        btn_add_course = tk.Button(
            nav_frame, 
            text="Add Course", 
            command=lambda: self.show_frame("course_form"),
            bg="#34495e",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=10,
            relief="flat"
        )
        btn_add_course.pack(side="left", padx=5, pady=5)
        
        btn_add_assignment = tk.Button(
            nav_frame, 
            text="Add Assignment", 
            command=lambda: self.show_frame("assignment_form"),
            bg="#34495e",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=10,
            relief="flat"
        )
        btn_add_assignment.pack(side="left", padx=5, pady=5)
    
    def show_frame(self, frame_name):
        """Switch to the specified frame."""
        # Destroy all existing widgets in content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create and display the requested frame
        if frame_name == "dashboard":
            frame = DashboardFrame(self.content_frame, self)
        elif frame_name == "course_form":
            frame = CourseFormFrame(self.content_frame, self)
        elif frame_name == "assignment_form":
            frame = AssignmentFormFrame(self.content_frame, self)
        else:
            frame = DashboardFrame(self.content_frame, self)
        
        frame.pack(fill="both", expand=True)
    
    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()
