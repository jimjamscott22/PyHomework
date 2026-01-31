"""
Dashboard view - main screen showing all assignments grouped by urgency
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.assignment import Assignment
from models.course import Course
from logic.deadline import categorize_assignment, format_due_datetime, parse_due_datetime
from logic.notifications import NotificationManager


class DashboardFrame(tk.Frame):
    """Dashboard frame displaying assignments by urgency."""

    def __init__(self, parent, app, theme_manager):
        self.app = app
        self.theme_manager = theme_manager
        colors = theme_manager.get_colors()
        super().__init__(parent, bg=colors['bg'])
        self.create_widgets()
    
    def create_widgets(self):
        """Create the dashboard layout."""
        colors = self.theme_manager.get_colors()

        # Title
        title = tk.Label(
            self,
            text="Assignment Dashboard - Spring 2026",
            font=("Arial", 18, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title.pack(pady=10)

        # Notification banner
        self.show_notification_banner()

        # Refresh button
        refresh_btn = tk.Button(
            self,
            text="Refresh",
            command=self.refresh_dashboard,
            bg=colors['button_primary'],
            fg=colors['button_fg'],
            font=("Arial", 10),
            padx=10,
            pady=5,
            relief="flat"
        )
        refresh_btn.pack(pady=5)

        # Scrollable frame for assignments
        canvas = tk.Canvas(self, bg=colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load assignments
        self.load_assignments()
    
    def load_assignments(self):
        """Load and display all assignments grouped by category."""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get all assignments and courses
        assignments = Assignment.get_all()
        courses = {c.id: c for c in Course.get_all()}
        
        # Categorize assignments
        categories = {
            'overdue': [],
            'due_today': [],
            'due_soon': [],
            'later': []
        }
        
        for assignment in assignments:
            category = categorize_assignment(assignment.due_datetime)
            categories[category].append(assignment)
        
        # Sort each category by due date
        for category in categories:
            categories[category].sort(
                key=lambda a: parse_due_datetime(a.due_datetime) or datetime.max
            )
        
        # Display each category
        colors = self.theme_manager.get_colors()
        self.display_category("Overdue", categories['overdue'], courses, colors['overdue'])
        self.display_category("Due Today", categories['due_today'], courses, colors['due_today'])
        self.display_category("Due Soon (Next 7 Days)", categories['due_soon'], courses, colors['due_soon'])
        self.display_category("Later This Semester", categories['later'], courses, colors['later'])
        
        # Show message if no assignments
        if not assignments:
            colors = self.theme_manager.get_colors()
            msg = tk.Label(
                self.scrollable_frame,
                text="No assignments yet. Add some using the navigation bar!",
                font=("Arial", 12),
                bg=colors['bg'],
                fg=colors['text_muted']
            )
            msg.pack(pady=50)
    
    def display_category(self, title, assignments, courses, color):
        """Display a category section with its assignments."""
        if not assignments:
            return  # Don't show empty categories
        
        # Category header
        header_frame = tk.Frame(self.scrollable_frame, bg=color, height=40)
        header_frame.pack(fill="x", pady=(10, 0), padx=10)
        
        header_label = tk.Label(
            header_frame,
            text=f"{title} ({len(assignments)})",
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            pady=8
        )
        header_label.pack(anchor="w", padx=10)
        
        # Assignment cards
        for assignment in assignments:
            self.display_assignment_card(assignment, courses)
    
    def display_assignment_card(self, assignment, courses):
        """Display a single assignment card."""
        from datetime import datetime
        colors = self.theme_manager.get_colors()

        # Card frame
        card = tk.Frame(
            self.scrollable_frame,
            bg=colors['card_bg'],
            relief="solid",
            borderwidth=1
        )
        card.pack(fill="x", pady=5, padx=20)

        # Course name
        course = courses.get(assignment.course_id)
        course_name = course.name if course else "Unknown Course"

        course_label = tk.Label(
            card,
            text=course_name,
            font=("Arial", 10, "bold"),
            bg=colors['card_bg'],
            fg=colors['card_fg']
        )
        course_label.pack(anchor="w", padx=10, pady=(5, 0))

        # Assignment title
        title_label = tk.Label(
            card,
            text=assignment.title,
            font=("Arial", 12),
            bg=colors['card_bg'],
            fg=colors['card_fg']
        )
        title_label.pack(anchor="w", padx=10)

        # Type and due date
        info_text = f"{assignment.type} • Due: {format_due_datetime(assignment.due_datetime)}"
        info_label = tk.Label(
            card,
            text=info_text,
            font=("Arial", 9),
            bg=colors['card_bg'],
            fg=colors['text_muted']
        )
        info_label.pack(anchor="w", padx=10)

        # Status
        status_label = tk.Label(
            card,
            text=f"Status: {assignment.status}",
            font=("Arial", 9),
            bg=colors['card_bg'],
            fg=colors['status_color']
        )
        status_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def show_notification_banner(self):
        """Display notification banner if there are upcoming assignments."""
        if not NotificationManager.should_show_notification():
            return

        upcoming = NotificationManager.get_upcoming_assignments()
        if not upcoming:
            return

        colors = self.theme_manager.get_colors()

        # Create notification banner
        banner = tk.Frame(
            self,
            bg=colors['notification_bg'],
            relief="solid",
            borderwidth=2,
            highlightbackground=colors['notification_border'],
            highlightthickness=1
        )
        banner.pack(fill="x", padx=20, pady=(0, 10))

        # Notification icon and message
        message = NotificationManager.format_notification_message(upcoming)
        msg_label = tk.Label(
            banner,
            text=f"⚠ {message}",
            font=("Arial", 11, "bold"),
            bg=colors['notification_bg'],
            fg=colors['notification_fg'],
            pady=10
        )
        msg_label.pack(anchor="w", padx=15)

        # Details
        details = NotificationManager.get_notification_details(upcoming)
        for detail in details[:3]:  # Show max 3 assignments
            detail_text = f"  • {detail['course']}: {detail['title']} - Due {detail['due']}"
            detail_label = tk.Label(
                banner,
                text=detail_text,
                font=("Arial", 9),
                bg=colors['notification_bg'],
                fg=colors['notification_fg'],
                anchor="w"
            )
            detail_label.pack(anchor="w", padx=15, pady=2)

        if len(upcoming) > 3:
            more_label = tk.Label(
                banner,
                text=f"  ... and {len(upcoming) - 3} more",
                font=("Arial", 9, "italic"),
                bg=colors['notification_bg'],
                fg=colors['notification_fg'],
                anchor="w",
                pady=5
            )
            more_label.pack(anchor="w", padx=15)

    def refresh_dashboard(self):
        """Refresh the dashboard to show updated assignments."""
        self.load_assignments()
