"""
Deadline calculation logic for assignments
Spring 2026 semester tracking
"""

from datetime import datetime, timedelta


# Spring 2026 semester dates (configurable constants)
SEMESTER_START = datetime(2026, 1, 12)  # Typical spring semester start
SEMESTER_END = datetime(2026, 5, 15)    # Typical spring semester end


def parse_due_datetime(due_str):
    """Parse a due datetime string to datetime object."""
    if isinstance(due_str, datetime):
        return due_str
    try:
        return datetime.fromisoformat(due_str)
    except (ValueError, TypeError):
        return None


def is_overdue(due_datetime):
    """Check if an assignment is overdue."""
    if due_datetime is None:
        return False
    now = datetime.now()
    return due_datetime < now


def is_due_today(due_datetime):
    """Check if an assignment is due today."""
    if due_datetime is None:
        return False
    now = datetime.now()
    return due_datetime.date() == now.date()


def is_due_soon(due_datetime, days=7):
    """Check if an assignment is due within the next N days (default 7)."""
    if due_datetime is None:
        return False
    now = datetime.now()
    # Due soon means: not overdue, not today, but within the next N days
    return now < due_datetime <= now + timedelta(days=days)


def is_later_this_semester(due_datetime):
    """Check if an assignment is due later this semester (beyond 7 days)."""
    if due_datetime is None:
        return False
    now = datetime.now()
    seven_days_from_now = now + timedelta(days=7)
    return due_datetime > seven_days_from_now and due_datetime <= SEMESTER_END


def categorize_assignment(due_datetime):
    """
    Categorize an assignment based on its due date.
    Returns: 'overdue', 'due_today', 'due_soon', or 'later'
    """
    due_dt = parse_due_datetime(due_datetime)
    
    if due_dt is None:
        return 'later'
    
    if is_overdue(due_dt):
        return 'overdue'
    elif is_due_today(due_dt):
        return 'due_today'
    elif is_due_soon(due_dt):
        return 'due_soon'
    elif is_later_this_semester(due_dt):
        return 'later'
    else:
        return 'later'


def format_due_datetime(due_datetime):
    """Format a datetime for display."""
    due_dt = parse_due_datetime(due_datetime)
    if due_dt is None:
        return "No date"
    return due_dt.strftime("%a, %b %d, %Y at %I:%M %p")
