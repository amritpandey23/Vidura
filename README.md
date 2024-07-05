# Vidura - Your personal work tracker

Vidura is my personal work tracker that helps me track your daily professional and personal tasks. It is a hobby project of mine and is available for anyone to use in development environment. Some features of this app are:

- Tasks: Create new tasks and revisit history.
- Logs: Add daily activity logs.
- Customization options.

Currently all these features are manual, however it is still in the beginning phase and I plan to automate the heck out of this thing. For example, I want the daily log to be filled based on the tasks that have been worked on. I also want to add gen ai based insight generation for my historical data.

## Setting development environment

As this is a web app and only runs locally, you'll have to perform setup manually.

### What you'll need?

- Python 3.11
- Pip 24 or latest
- Virtual environment

### Setup

1. Clone the repo.
2. Create virtual environment inside the repo: `python -m venv .venv`.
3. Activate environment: `. .venv/Scripts/activate`, if you are on mac then: `. .venv/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Launch: `python start.py`.

## Database location

By default database is stored in the user directory with the name `site.db`. You can also navigate to `/settings` route to find the exact directory path in settings section.
