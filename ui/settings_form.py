"""
Settings form view - user preferences and configuration
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.settings import Settings


class SettingsFormFrame(tk.Frame):
    """Frame for managing user settings."""

    def __init__(self, parent, app, theme_manager):
        self.app = app
        self.theme_manager = theme_manager
        colors = theme_manager.get_colors()
        super().__init__(parent, bg=colors['bg'])
        self.create_widgets()

    def create_widgets(self):
        """Create the settings form layout."""
        colors = self.theme_manager.get_colors()

        # Title
        title = tk.Label(
            self,
            text="Settings",
            font=("Arial", 18, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        title.pack(pady=10)

        # Form frame
        form_frame = tk.Frame(self, bg=colors['bg'])
        form_frame.pack(pady=20, padx=50, fill="x")

        # Appearance Section
        appearance_label = tk.Label(
            form_frame,
            text="Appearance",
            font=("Arial", 14, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        appearance_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 5))

        # Theme selection
        tk.Label(
            form_frame,
            text="Theme:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.theme_var = tk.StringVar()
        theme_options = ["light", "dark"]
        self.theme_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.theme_var,
            values=theme_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.theme_dropdown.grid(row=1, column=1, pady=5, padx=10)
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.preview_theme)

        # Separator
        ttk.Separator(form_frame, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=15
        )

        # Notifications Section
        notifications_label = tk.Label(
            form_frame,
            text="Notifications",
            font=("Arial", 14, "bold"),
            bg=colors['bg'],
            fg=colors['fg']
        )
        notifications_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 5))

        # Enable notifications
        tk.Label(
            form_frame,
            text="Enable Notifications:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=4, column=0, sticky="w", pady=5)

        self.notifications_var = tk.BooleanVar()
        self.notifications_check = tk.Checkbutton(
            form_frame,
            variable=self.notifications_var,
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['bg'],
            activeforeground=colors['fg'],
            selectcolor=colors['card_bg']
        )
        self.notifications_check.grid(row=4, column=1, sticky="w", pady=5, padx=10)

        # Days before due date
        tk.Label(
            form_frame,
            text="Notify Days Before Due:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=5, column=0, sticky="w", pady=5)

        self.days_var = tk.StringVar()
        days_options = ["1", "2", "3", "5", "7"]
        self.days_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.days_var,
            values=days_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.days_dropdown.grid(row=5, column=1, pady=5, padx=10)

        # Notification time
        tk.Label(
            form_frame,
            text="Notification Time:",
            font=("Arial", 11),
            bg=colors['bg'],
            fg=colors['fg']
        ).grid(row=6, column=0, sticky="w", pady=5)

        self.time_var = tk.StringVar()
        time_options = ["08:00", "09:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
        self.time_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.time_var,
            values=time_options,
            state="readonly",
            font=("Arial", 11),
            width=37
        )
        self.time_dropdown.grid(row=6, column=1, pady=5, padx=10)

        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=colors['bg'])
        buttons_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Save button
        save_btn = tk.Button(
            buttons_frame,
            text="Save Settings",
            command=self.save_settings,
            bg=colors['button_success'],
            fg=colors['button_fg'],
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            relief="flat"
        )
        save_btn.pack(side="left", padx=5)

        # Reset button
        reset_btn = tk.Button(
            buttons_frame,
            text="Reset to Defaults",
            command=self.reset_to_defaults,
            bg=colors['text_muted'],
            fg=colors['button_fg'],
            font=("Arial", 11),
            padx=20,
            pady=8,
            relief="flat"
        )
        reset_btn.pack(side="left", padx=5)

        # Load current settings
        self.load_current_settings()

    def load_current_settings(self):
        """Load current settings from database."""
        settings = Settings.get_all()

        # Set theme
        self.theme_var.set(settings.get('theme_mode', 'light'))

        # Set notifications
        notifications_enabled = settings.get('notifications_enabled', 'true') == 'true'
        self.notifications_var.set(notifications_enabled)

        # Set days before
        self.days_var.set(settings.get('notification_days_before', '1'))

        # Set notification time
        self.time_var.set(settings.get('notification_time', '09:00'))

    def preview_theme(self, event=None):
        """Preview theme change without saving."""
        new_theme = self.theme_var.get()
        self.theme_manager.switch_theme(new_theme)
        # Refresh current view to show theme change
        self.app.show_frame("settings")

    def save_settings(self):
        """Save settings to database."""
        try:
            # Save theme
            Settings.set('theme_mode', self.theme_var.get())

            # Save notifications
            notifications_enabled = 'true' if self.notifications_var.get() else 'false'
            Settings.set('notifications_enabled', notifications_enabled)

            # Save days before
            Settings.set('notification_days_before', self.days_var.get())

            # Save notification time
            Settings.set('notification_time', self.time_var.get())

            # Apply theme
            self.theme_manager.switch_theme(self.theme_var.get())

            messagebox.showinfo("Success", "Settings saved successfully!")

            # Refresh current view
            self.app.show_frame("settings")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        response = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to their defaults?"
        )

        if response:
            try:
                # Reset to defaults
                for key, value in Settings.DEFAULTS.items():
                    Settings.set(key, value)

                # Reload settings
                self.load_current_settings()

                # Apply default theme
                self.theme_manager.switch_theme('light')

                messagebox.showinfo("Success", "Settings reset to defaults!")

                # Refresh current view
                self.app.show_frame("settings")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")
