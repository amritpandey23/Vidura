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

Here's an improved version of your development guide:

## Development Guide

Welcome to the development guide for our project. This guide will help you understand how to contribute effectively.

### Creating Pull Requests and Issues

- **Creating Issues**: Navigate to the Issues tab and create a new issue. Ensure you add appropriate labels such as `enhancement`, `bug`, etc. Only collaborators can add version labels.
- **Creating Pull Requests**:
  1. Fork this repository.
  2. Create a pull request (PR) against the latest development or fix branch.
  3. Do not create PRs for the master branch.

### Release Versions

We follow the `MAJOR.MINOR.PATCH` versioning convention:

- **Bug Fixes**:
  - Branch naming convention: `Fix-x.y.z`.
  - Example: If the current release is `1.0.0`, the bug fix branch will be `Fix-1.0.1`.
- **Minor Releases and Development**:
  - Branch naming convention: `Develop-x.y.z`.
  - Example: If the current release is `1.0.1` or `1.0.0`, the minor development branch will be `Develop-1.1.1` or `Develop-1.1.0`.

Each minor development and fix branch is closed weekly, after which the version is incremented by one. For major release there is no timeline. Usually the work on the major branch will go parallely with the other branches.

### Changelog

- Update the `changelog.md` file in the root directory with a description of changes made in each PR.

Feel free to reach out with any questions or feedback. Happy coding!

## License

Released under MIT License

Copyright (c) 2024 Amrit Pandey.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
