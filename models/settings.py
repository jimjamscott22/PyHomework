"""
User settings model and database operations
"""

from db.database import get_connection


class Settings:
    """Manages user preferences and settings."""

    # Default settings
    DEFAULTS = {
        'theme_mode': 'light',
        'notifications_enabled': 'true',
        'notification_days_before': '1',
        'notification_time': '09:00'
    }

    @staticmethod
    def get(key, default=None):
        """Get a setting value by key."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT setting_value FROM user_settings WHERE setting_key = ?", (key,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return row["setting_value"]
        return default if default is not None else Settings.DEFAULTS.get(key)

    @staticmethod
    def set(key, value):
        """Set a setting value (INSERT or UPDATE)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO user_settings (setting_key, setting_value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (key, str(value))
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """Get all settings as a dictionary."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT setting_key, setting_value FROM user_settings")
        rows = cursor.fetchall()
        conn.close()

        # Start with defaults and override with database values
        settings = Settings.DEFAULTS.copy()
        for row in rows:
            settings[row["setting_key"]] = row["setting_value"]

        return settings

    @staticmethod
    def initialize_defaults():
        """Initialize default settings if they don't exist."""
        existing_settings = Settings.get_all()

        # Only insert defaults that don't already exist
        for key, value in Settings.DEFAULTS.items():
            if key not in existing_settings or existing_settings[key] is None:
                Settings.set(key, value)
