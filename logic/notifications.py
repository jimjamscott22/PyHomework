"""
Notification logic for assignment reminders
"""

from datetime import datetime, timedelta
from models.assignment import Assignment
from models.course import Course
from models.settings import Settings
from logic.deadline import parse_due_datetime


class NotificationManager:
    """Manages assignment due date notifications."""

    @staticmethod
    def get_upcoming_assignments():
        """Get assignments due within notification window."""
        # Check if notifications are enabled
        notifications_enabled = Settings.get('notifications_enabled', 'true') == 'true'
        if not notifications_enabled:
            return []

        # Get notification settings
        days_before = int(Settings.get('notification_days_before', '1'))

        # Get all assignments
        assignments = Assignment.get_all()

        # Filter assignments by due date
        upcoming = []
        now = datetime.now()
        notification_window = now + timedelta(days=days_before)

        for assignment in assignments:
            due_dt = parse_due_datetime(assignment.due_datetime)
            if due_dt and now <= due_dt <= notification_window:
                # Only notify for assignments not yet submitted
                if assignment.status != "Submitted":
                    upcoming.append(assignment)

        return upcoming

    @staticmethod
    def should_show_notification():
        """Check if notifications are enabled and time is right."""
        notifications_enabled = Settings.get('notifications_enabled', 'true') == 'true'
        if not notifications_enabled:
            return False

        # For in-app notifications, we'll always show if there are upcoming assignments
        # The notification_time setting can be used for future desktop notifications
        return True

    @staticmethod
    def format_notification_message(assignments):
        """Format assignments into notification message."""
        if not assignments:
            return ""

        count = len(assignments)
        if count == 1:
            assignment = assignments[0]
            return f"You have 1 assignment due soon: {assignment.title}"
        else:
            return f"You have {count} assignments due soon"

    @staticmethod
    def get_notification_details(assignments):
        """Get detailed list of assignments for notification banner."""
        if not assignments:
            return []

        details = []
        courses = {c.id: c for c in Course.get_all()}

        for assignment in assignments:
            course = courses.get(assignment.course_id)
            course_name = course.name if course else "Unknown Course"

            due_dt = parse_due_datetime(assignment.due_datetime)
            if due_dt:
                due_str = due_dt.strftime("%b %d at %I:%M %p")
            else:
                due_str = assignment.due_datetime

            details.append({
                'title': assignment.title,
                'course': course_name,
                'due': due_str
            })

        return details
