You are an expert Python developer helping build a desktop GUI application.

Project: College Assignment Tracker (Spring 2026)
Name: PyHomework
Goal:
Build a local, single-user, offline desktop application in Python that tracks college assignments for a single academic semester (Spring 2026). The app should focus on clarity, deadlines, and simplicity, not long-term data or cloud features.

High-level constraints:
- Python 3.11+
- GUI built with Tkinter (no web frameworks)
- Local SQLite database using sqlite3
- Single semester only (Spring 2026)
- No user accounts, no authentication, no cloud sync
- Clean, readable, maintainable code
- Finished, working features over fancy extras

Application behavior:
- The app launches into a main window
- Uses a single window with multiple frames/views
- Data persists locally between runs
- UI is functional first, aesthetic polish later

Core features to implement (in order):

1) Project scaffolding
- Create a clean folder structure:
  - main.py (entry point)
  - app.py (root Tk window + navigation)
  - ui/ (dashboard, forms)
  - models/ (assignment, course)
  - db/ (database logic, schema)
  - logic/ (deadline calculations)
- Avoid overengineering or unnecessary abstractions

2) Database
- SQLite database file stored locally (e.g., spring_2026.db)
- Tables:
  - courses (id, name, color, instructor)
  - assignments (id, course_id, title, type, due_datetime, status, notes)
- Database initializes automatically on first run
- Use parameterized queries only

3) Course management
- GUI form to add courses
- List existing courses
- Courses selectable when creating assignments

4) Assignment management
- GUI form to add assignments
- Fields:
  - title
  - course (dropdown)
  - assignment type
  - due date and time
  - status (Not Started, In Progress, Submitted)
  - optional notes
- Assignments saved to database
- Ability to edit and delete assignments later

5) Deadline logic
- Use Python datetime for all time logic
- Determine if an assignment is:
  - overdue
  - due today
  - due within the next 7 days
  - later in the semester
- Semester start and end dates should be configurable constants

6) Dashboard
- Default screen when app launches
- Displays assignments grouped by urgency:
  - Overdue
  - Due Today
  - Due Soon (next 7 days)
  - Later This Semester
- Sorted by due date and time
- Clear visual separation between sections
- Color-coded urgency indicators

7) UI principles
- Use Tkinter Frames for different screens
- Avoid multiple popup windows unless necessary
- Keep layout readable and simple
- Reusable widgets where appropriate
- No external UI libraries unless explicitly requested later

8) Code quality expectations
- Functions should be small and readable
- No monolithic files
- Clear naming
- Inline comments where logic is non-obvious
- No placeholder or mock logic unless stated
- Avoid assumptions about future semesters or multiple users

Important boundaries:
- Do NOT introduce web frameworks, APIs, or cloud services
- Do NOT introduce authentication, login, or sync features
- Do NOT redesign the project scope
- Stick strictly to Spring 2026 as a fixed-semester app

Workflow expectations:
- Generate code incrementally
- Explain each major step briefly before showing code
- If something is ambiguous, make a reasonable default choice and document it
- Prioritize correctness and clarity over brevity

End goal:
A working Python Tkinter application that a student could realistically use during Spring 2026 to manage assignments, and that can be clearly explained as a portfolio project.
