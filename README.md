# Vidura - Personal Work Tracker

Vidura is my personal work tracker designed to help me manage my daily professional and personal tasks. It's a hobby project that's available for use in a development environment. Key features include:

- **Tasks**: Create new tasks and revisit task history.
- **Logs**: Add daily activity logs.
- **Customization**: Various customization options available.

## Setting Up the Development Environment

Vidura is a web app that runs locally, so you'll need to set it up manually.

### Requirements

- Python 3.11
- Pip 24 or later
- Virtual environment

### Setup Instructions

1. Clone the repository.
2. Create a virtual environment inside the repository: `python -m venv .venv`.
3. Activate the virtual environment:
   - On Windows: `. .venv/Scripts/activate`
   - On macOS/Linux: `. .venv/bin/activate`
4. Install the dependencies: `pip install -r requirements.txt`.
5. Launch the application: `python start.py`.

## Customization

### Database File

By default, the database is stored in the user directory under the name `site.db`. You can also navigate to the `/settings` route to find the exact directory path in the settings section.

### Important Dates

Important dates can be added in a JSON file, which can be edited via the `/settings` route.

### Notes

To add notes, such as important links or other information on home page, use the JSON field in the `/settings` route. An example format is provided.
