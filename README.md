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

Changes can be made to the app by changing the available settings in the `/settings` route. For app level settings changes a manual restart of the app is required.

### Database File

By default, the database is stored in the user directory under the name `site.db`. You can also navigate to the `/settings` route to find the exact directory path in the settings section.

### Important Dates

Important dates can be added in a JSON file, which can be edited via the `/settings` route.

### Notes

To add notes, such as important links or other information on home page, use the JSON field in the `/settings` route. An example format is provided.

## License

Released under MIT License

Copyright (c) 2024 Amrit Pandey.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
