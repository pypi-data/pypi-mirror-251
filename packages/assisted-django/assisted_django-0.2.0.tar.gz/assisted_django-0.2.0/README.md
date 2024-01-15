# Assisted Django

A CLI Tool to generate content for all files in a django app directory including templates with the help of openai models

This script would generate the following files for you:
- [x] models.py
- [x] views.py
- [x] urls.py
- [x] admin.py
- [x] tests.py
- [x] forms.py
- [x] signals.py
- [x] HTML templates

> Meant to be run after the startapp command

### Installation

`pip install assisted-django`

##### Usage

1. Make a django project and create a new app as usual
2. Run `python -m assisted_django` in the same level as `manage.py`
3. `CLI` will guide you through the rest of the process

### Additional Notes
- Set the `OPENAI_API_KEY` in your `.env` file
- This script **will overwrite** the existing app directory files
- The CLI will confirm with the full file path before taking any action
- **Write better briefs to get better results**

### Some More Context
- We prefer class based generic views
- We utilize django-crispy-forms with bootstrap4
- Html templates utilize bootstrap4
