# Assisted Django

Assisted Django is a python package that uses OpenAI's gpt-3 / 4 to generate Django code based on a project brief.

This script would generate the following files for you:
- [x] models.py
- [x] views.py
- [x] urls.py
- [x] admin.py
- [x] tests.py
- [x] forms.py
- [x] signals.py
- [x] HTML templates

You can also let the script generate the detailed project brief by passing `better_brief=True` to the `generate` method.

> This script is not meant to replace the startapp command, but meant to be run after the startapp command has generated the basic files. However, you do not need to create the additional files (such as forms.py, signals.py, tests.py, urls.py etc) as this script will create them for you.

### Example Video

https://github.com/fauzaanu/assisted-django/assets/86226565/6c5d9b8a-68c8-4883-a65d-c08c41fbb913

##### Example of how to run this: (Video is outdated, and before template generation was added)

1. Make a django project and create a new app as usual
2. `pip install assisted-django`
3. On the same level as manage.py, create a python file (generate.py for example)
4. Use the code below as a template, and replace the app_name, app_directory, and purpose variables with your own.
5. before running set the `OPENAI_API_KEY` environment variable to your openai api key

```python
from assisted_django.DjangoApplication import DjangoApplication


def enhance_django_app():
    app_name = "fakebook_clone"  # replace with your actual Django app name (NOT PROJECT NAME)
    app_directory = "Basic/fakebook_clone"  # replace with your actual Django app directory (ProjectDir/Appdir)

    with open("../fakebook_clone", "r") as f:  # Replace with your actual Project Brief
        purpose = f.read()

    django_app = DjangoApplication(app_name, purpose, app_directory)
    django_app.generate(better_brief=True) # better_brief=True would generate a better brief first


if __name__ == '__main__':
    enhance_django_app()
```
