import os
import typer


# def enhance_django_app():
#     app_name = "fakebook_clone"  # replace with your actual Django app name
#     app_directory = "Basic/fakebook_clone"  # replace with your actual Django app directory
#
#     with open("../fakebook_clone", "r") as f:  # Replace "README.md" with your actual README file
#         purpose = f.read()
#
#     django_app = DjangoApplication(app_name, purpose, app_directory)
#     django_app.generate(better_brief=True)
#
#
# if __name__ == '__main__':
#     enhance_django_app()

# convert to CLI and to be dynamic
# 1. Scan for Django apps
# 2. Keep the correct app_name in memory
# 3. Keep the correct app_directory in memory
# 4. ask the user to pick the brief file (is it readme or is it another file?)
# 5. Read the brief file, keep it in memory
# 6. Ask the user if they want to generate a better brief
# 7. if yes call generate with better_brief=True
class AssistedDjangoCLI:
    def __init__(self):
        self.scan_for_apps()

    def scan_for_apps(self):
        """
        Scans for Django apps in the current directory.
        """

        if not os.path.exists("manage.py"):
            typer.echo("Please run this command from the root of your Django project.")
            raise typer.Exit()

        django_apps = []
        required_files = ["models.py", "views.py", "urls.py", "admin.py", "tests.py", "forms.py"]
        for root, dirs, files in os.walk(".."):
            if all(file in files for file in required_files):
                app_name = root.split(os.path.sep)[-1]
                django_apps.append(app_name)

        if django_apps:
            typer.echo("Django Apps found:")
            for app in django_apps:
                typer.echo(f"- {app}")
        else:
            typer.echo("No Django Apps found.")


if __name__ == "__main__":
    typer.run(AssistedDjangoCLI)
