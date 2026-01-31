"""
Course form view - add and list courses
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.course import Course


class CourseFormFrame(tk.Frame):
    """Frame for adding courses and viewing the course list."""

    def __init__(self, parent, app, theme_manager):
        self.app = app
        self.theme_manager = theme_manager
        colors = theme_manager.get_colors()
        super().__init__(parent, bg=colors['bg'])
        self.create_widgets()
    
    def create_widgets(self):
        """Create the course form layout."""
        colors = self.theme_manager.get_colors()

        # Title
        title = tk.Label(
            self,
            text="Add Course",
            font=("Arial", 18, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title.pack(pady=10)

        # Form frame
        form_frame = tk.Frame(self, bg=colors['bg'])
        form_frame.pack(pady=20, padx=50, fill="x")

        # Course name
        tk.Label(
            form_frame,
            text="Course Name:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=40,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)

        # Instructor
        tk.Label(
            form_frame,
            text="Instructor:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=1, column=0, sticky="w", pady=5)
        self.instructor_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            width=40,
            bg=colors['card_bg'],
            fg=colors['card_fg'],
            insertbackground=colors['fg']
        )
        self.instructor_entry.grid(row=1, column=1, pady=5, padx=10)

        # Color (optional visual indicator)
        tk.Label(
            form_frame,
            text="Color Tag:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=2, column=0, sticky="w", pady=5)
        self.color_var = tk.StringVar(value="Blue")
        color_options = ["Blue", "Green", "Red", "Orange", "Purple", "Yellow"]
        self.color_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.color_var,
            values=color_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.color_dropdown.grid(row=2, column=1, pady=5, padx=10)

        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="Add Course",
            command=self.add_course,
            bg=colors['button_success'],
            fg=colors['button_fg'],
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief="flat"
        )
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Divider
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=20, padx=50)

        # Existing courses section
        courses_title = tk.Label(
            self,
            text="Existing Courses",
            font=("Arial", 14, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        courses_title.pack(pady=10)

        # Scrollable course list
        self.courses_frame = tk.Frame(self, bg=colors['bg'])
        self.courses_frame.pack(fill="both", expand=True, padx=50, pady=10)

        self.load_courses()
    
    def add_course(self):
        """Add a new course to the database."""
        name = self.name_entry.get().strip()
        instructor = self.instructor_entry.get().strip()
        color = self.color_var.get()
        
        if not name:
            messagebox.showwarning("Input Error", "Please enter a course name.")
            return
        
        try:
            Course.create(name, color, instructor)
            messagebox.showinfo("Success", f"Course '{name}' added successfully!")
            
            # Clear form
            self.name_entry.delete(0, tk.END)
            self.instructor_entry.delete(0, tk.END)
            self.color_var.set("Blue")
            
            # Refresh course list
            self.load_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")
    
    def load_courses(self):
        """Load and display all courses."""
        colors = self.theme_manager.get_colors()

        # Clear existing course widgets
        for widget in self.courses_frame.winfo_children():
            widget.destroy()

        courses = Course.get_all()

        if not courses:
            msg = tk.Label(
                self.courses_frame,
                text="No courses yet.",
                font=("Arial", 11),
                bg=colors['bg'],
                fg=colors['text_muted']
            )
            msg.pack(pady=20)
            return

        # Display each course
        for course in courses:
            course_card = tk.Frame(
                self.courses_frame,
                bg=colors['card_bg'],
                relief="solid",
                borderwidth=1
            )
            course_card.pack(fill="x", pady=5)

            # Course info
            info_text = f"{course.name}"
            if course.instructor:
                info_text += f" • {course.instructor}"
            info_text += f" • {course.color}"

            course_label = tk.Label(
                course_card,
                text=info_text,
                font=("Arial", 11),
                bg=colors['card_bg'],
                fg=colors['card_fg'],
                anchor="w"
            )
            course_label.pack(fill="x", padx=10, pady=8)
