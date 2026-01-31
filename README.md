# PyHomework

A small Python project to manage courses, assignments, and deadlines with a minimal UI and local database modules.

## Features

- Track assignments and courses
- Manage deadlines and related logic
- Minimal UI components for creating/editing assignments and courses
- Simple DB abstraction for local persistence

## Requirements

- Python 3.8+
- (Optional) virtual environment for development

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/jimjamscott22/PyHomework.git
cd PyHomework
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (if you add a `requirements.txt` later). There are no pinned dependencies in the repo currently.

```bash
pip install -r requirements.txt  # if present
```

4. Run the application. The repository contains both `main.py` and `app.py` — run whichever entrypoint your setup expects:

```bash
python main.py
# or
python app.py
```

If the project uses a specific framework or CLI, check the source for how the app starts.

## Project Structure

Below are the main files and directories with short descriptions:

- [app.py](app.py): Possible application entrypoint or launcher.
- [main.py](main.py): Alternate entrypoint; inspect to confirm runtime behavior.
- [db/](db): Database abstraction and initialization.
  - [db/database.py](db/database.py): Database access layer and helpers.
- [logic/](logic): Business logic modules.
  - [logic/deadline.py](logic/deadline.py): Deadline calculations and helpers.
- [models/](models): Domain models for the app.
  - [models/assignment.py](models/assignment.py): `Assignment` model and fields.
  - [models/course.py](models/course.py): `Course` model and fields.
- [ui/](ui): UI components (forms, dashboard).
  - [ui/assignment_form.py](ui/assignment_form.py): Assignment creation/editing form.
  - [ui/course_form.py](ui/course_form.py): Course creation/editing form.
  - [ui/dashboard.py](ui/dashboard.py): Main UI/dashboard view.

## Development

- Editing: Update modules in `models/`, `logic/`, and `ui/` to add features.
- Persistence: See `db/database.py` for how data is stored/loaded.
- Tests: No tests are included by default — consider adding a `tests/` directory and using `pytest`.

Recommended commands while developing:

```bash
# Run the app
python main.py

# Linting / formatting (if you add tooling)
black .
flake8 .
```

## Contributing

Contributions are welcome. Good first steps:

- Open an issue describing the feature or bug.
- Create a branch, implement the change, and open a pull request.

If you plan to contribute, consider adding a `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

## License

No license file is included in the repository. If you want to open-source this project, add a `LICENSE` file (for example, MIT).

## Contact

Repository owner: `jimjamscott22` (GitHub)

---

If you'd like, I can also:

- add a `requirements.txt` by detecting imported packages,
- add a `LICENSE` (e.g., MIT),
- or update the README with exact run instructions after you confirm which file (`main.py` or `app.py`) is the real entrypoint.
