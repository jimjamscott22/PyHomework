"""
Theme management for the application
Handles light/dark mode switching and color schemes
"""

import tkinter as tk
from tkinter import ttk


class ThemeManager:
    """Manages application theming and color schemes."""

    THEMES = {
        'light': {
            'bg': 'white',
            'fg': '#2c3e50',
            'nav_bg': '#2c3e50',
            'nav_fg': 'white',
            'nav_btn_bg': '#34495e',
            'card_bg': '#ecf0f1',
            'card_fg': '#2c3e50',
            'button_primary': '#3498db',
            'button_success': '#27ae60',
            'button_fg': 'white',
            'text_muted': '#7f8c8d',
            'overdue': '#e74c3c',
            'due_today': '#f39c12',
            'due_soon': '#f1c40f',
            'later': '#95a5a6',
            'status_color': '#16a085',
            'notification_bg': '#fff3cd',
            'notification_fg': '#856404',
            'notification_border': '#ffc107'
        },
        'dark': {
            'bg': '#1e1e1e',
            'fg': '#e0e0e0',
            'nav_bg': '#1a1a1a',
            'nav_fg': '#e0e0e0',
            'nav_btn_bg': '#2a2a2a',
            'card_bg': '#2a2a2a',
            'card_fg': '#e0e0e0',
            'button_primary': '#2980b9',
            'button_success': '#229954',
            'button_fg': 'white',
            'text_muted': '#a0a0a0',
            'overdue': '#e74c3c',
            'due_today': '#e67e22',
            'due_soon': '#f39c12',
            'later': '#7f8c8d',
            'status_color': '#1abc9c',
            'notification_bg': '#3a3a1a',
            'notification_fg': '#f0e68c',
            'notification_border': '#8b8000'
        }
    }

    def __init__(self, root, initial_theme='light'):
        """
        Initialize the theme manager.

        Args:
            root: The Tkinter root window
            initial_theme: Initial theme name ('light' or 'dark')
        """
        self.root = root
        self.current_theme = initial_theme
        self.configure_ttk_styles()

    def get_colors(self):
        """Get current theme colors."""
        return self.THEMES[self.current_theme]

    def configure_ttk_styles(self):
        """Configure ttk widget styles for current theme."""
        style = ttk.Style()
        colors = self.get_colors()

        # Configure Combobox
        style.configure(
            'TCombobox',
            fieldbackground=colors['card_bg'],
            background=colors['card_bg'],
            foreground=colors['fg'],
            arrowcolor=colors['fg']
        )

        # Configure Scrollbar
        style.configure(
            'Vertical.TScrollbar',
            background=colors['card_bg'],
            troughcolor=colors['bg'],
            arrowcolor=colors['fg']
        )

        # Configure Separator
        style.configure(
            'TSeparator',
            background=colors['text_muted']
        )

        # Configure Button
        style.configure(
            'TButton',
            background=colors['button_primary'],
            foreground=colors['button_fg'],
            borderwidth=0,
            focuscolor='none'
        )

        # Map button states
        style.map(
            'TButton',
            background=[('active', colors['button_primary'])],
            foreground=[('active', colors['button_fg'])]
        )

    def switch_theme(self, new_theme):
        """
        Switch to a different theme.

        Args:
            new_theme: New theme name ('light' or 'dark')
        """
        if new_theme in self.THEMES:
            self.current_theme = new_theme
            self.configure_ttk_styles()

    def get_theme_name(self):
        """Get the current theme name."""
        return self.current_theme
