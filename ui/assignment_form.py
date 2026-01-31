"""
Assignment form view - add, edit, and delete assignments
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.assignment import Assignment
from models.course import Course


class AssignmentFormFrame(tk.Frame):
    """Frame for adding and managing assignments."""

    def __init__(self, parent, app, theme_manager):
        self.app = app
        self.theme_manager = theme_manager
        colors = theme_manager.get_colors()
        super().__init__(parent, bg=colors['bg'])
        self.create_widgets()
    
    def create_widgets(self):
        """Create the assignment form layout."""
        colors = self.theme_manager.get_colors()

        # Title
        title = tk.Label(
            self,
            text="Add Assignment",
            font=("Arial", 18, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title.pack(pady=10)

        # Form frame
        form_frame = tk.Frame(self, bg=colors['bg'])
        form_frame.pack(pady=20, padx=50, fill="x")

        # Assignment title
        tk.Label(
            form_frame,
            text="Assignment Title:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=40,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.title_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Course selection
        tk.Label(
            form_frame,
            text="Course:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=1, column=0, sticky="w", pady=5)
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.course_var,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.course_dropdown.grid(row=1, column=1, pady=5, padx=10)
        self.load_courses()

        # Assignment type
        tk.Label(
            form_frame,
            text="Type:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=2, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="Homework")
        type_options = ["Homework", "Project", "Exam", "Quiz", "Lab", "Reading", "Other"]
        self.type_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.type_var,
            values=type_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.type_dropdown.grid(row=2, column=1, pady=5, padx=10)

        # Due date
        tk.Label(
            form_frame,
            text="Due Date (YYYY-MM-DD):",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=3, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=40,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.date_entry.grid(row=3, column=1, pady=5, padx=10)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Due time
        tk.Label(
            form_frame,
            text="Due Time (HH:MM):",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=4, column=0, sticky="w", pady=5)
        self.time_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=40,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.time_entry.grid(row=4, column=1, pady=5, padx=10)
        self.time_entry.insert(0, "23:59")

        # Status
        tk.Label(
            form_frame,
            text="Status:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=5, column=0, sticky="w", pady=5)
        self.status_var = tk.StringVar(value="Not Started")
        status_options = ["Not Started", "In Progress", "Submitted"]
        self.status_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=status_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.status_dropdown.grid(row=5, column=1, pady=5, padx=10)

        # Notes
        tk.Label(
            form_frame,
            text="Notes (optional):",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=6, column=0, sticky="nw", pady=5)
        self.notes_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            width=40,
            height=4,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.notes_text.grid(row=6, column=1, pady=5, padx=10)

        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="Add Assignment",
            command=self.add_assignment,
            bg=colors['button_primary'],
            fg=colors['button_fg'],
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief="flat"
        )
        submit_btn.grid(row=7, column=0, columnspan=2, pady=20)
    
    def load_courses(self):
        """Load available courses into the dropdown."""
        courses = Course.get_all()
        if courses:
            course_names = [f"{c.id}: {c.name}" for c in courses]
            self.course_dropdown["values"] = course_names
            if course_names:
                self.course_dropdown.current(0)
        else:
            self.course_dropdown["values"] = ["No courses available"]
            messagebox.showinfo("No Courses", "Please add courses first before creating assignments.")
    
    def add_assignment(self):
        """Add a new assignment to the database."""
        title = self.title_entry.get().strip()
        course_str = self.course_var.get()
        type_val = self.type_var.get()
        date_str = self.date_entry.get().strip()
        time_str = self.time_entry.get().strip()
        status = self.status_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        
        # Validation
        if not title:
            messagebox.showwarning("Input Error", "Please enter an assignment title.")
            return
        
        if not course_str or course_str == "No courses available":
            messagebox.showwarning("Input Error", "Please select a course.")
            return
        
        # Extract course ID
        try:
            course_id = int(course_str.split(":")[0])
        except:
            messagebox.showerror("Error", "Invalid course selection.")
            return
        
        # Parse date and time
        try:
            due_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Input Error", "Invalid date or time format.\nUse YYYY-MM-DD for date and HH:MM for time.")
            return
        
        # Save to database
        try:
            Assignment.create(course_id, title, type_val, due_datetime, status, notes)
            messagebox.showinfo("Success", f"Assignment '{title}' added successfully!")
            
            # Clear form
            self.title_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, "23:59")
            self.notes_text.delete("1.0", tk.END)
            self.status_var.set("Not Started")
            self.type_var.set("Homework")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add assignment: {str(e)}")
