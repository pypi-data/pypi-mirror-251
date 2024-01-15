import os

from dotenv import load_dotenv
from rich import print
from rich.panel import Panel
from rich import print
import typer
import typer.main

from .Assist.DjangoApplication import DjangoApplication


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

        print(Panel(renderable="CLI Tool to generate code for a singular django app"
                               "with the help of GPT3/4", highlight=True,
                    border_style="bold green", title="ASSISTED DJANGO",
                    subtitle="by @fauzaanu | https://t.me/fauzaanu"))

        # # if env is not set
        # NOT WORKING AS EXPECTED TODO: FIX
        # load_dotenv()
        # if not os.getenv("OPENAI_API_KEY"):
        #     print("Please set OPENAI_API_KEY in your .env file")
        #     raise typer.Exit()

        self.scan_for_apps()

    def scan_for_apps(self):
        """
        Scans for Django apps in the current directory.
        """

        if not os.path.exists("manage.py"):
            # typer.echo("Please run this command from the root of your Django project.")
            print("Please run this command from the root of your Django project. :frowning:")
            raise typer.Exit()

        django_apps = []
        required_files = ["__init__.py", "models.py"]

        # grab all the directories in the current directory
        directories = next(os.walk("."))[1]
        # print(directories)
        for directory in directories:
            # check if the directory has the required files
            if all(file in os.listdir(directory) for file in required_files):
                django_apps.append(directory)

        if django_apps:
            # Map the apps to numbers
            app_map = {}
            for index, app in enumerate(django_apps):
                app_map[index] = app

            # Print the apps with their full paths
            print("[bold green]Django Apps found[/bold green]")
            for index, app in app_map.items():
                app_path = os.path.abspath(app)
                typer.echo(
                    typer.style(f"{index + 1}. {app} - {app_path}", fg=typer.colors.BRIGHT_RED))

            # Ask the user to pick an app
            app_index = typer.prompt("\nWhich app would you like assistance with?", type=int)

            app_name = app_map[app_index - 1]
            appdir = os.path.abspath(app_name)

            print(f"[bold blue]App name[/bold blue] [yellow]{app_name}[/yellow]")
            print(f"[bold blue]App directory[/bold blue] [yellow]{appdir}[/yellow]")

            def check_for_briefs(directory=appdir):
                brief_files = []

                for item in os.listdir(directory):
                    if os.path.isdir(item):
                        continue
                    elif item.endswith(".md"):
                        # check if there is at least 1 line in the file
                        fullpath = os.path.join(directory, item)
                        with open(fullpath, "r") as f:
                            lines = f.readlines()
                            if len(lines) > 0:
                                brief_files.append((item, fullpath))

                return progress_brief_file(brief_files, appdir)

            def progress_brief_file(brief_files, appdir):
                if brief_files:
                    print("\n[bold green]Briefs found for[/bold green] [yellow]{}[/yellow]".format(app_name))
                    for index, (file, fullpath) in enumerate(brief_files):
                        typer.echo(typer.style(f"{index + 1}. {file} - {fullpath}",
                                               fg=typer.colors.BRIGHT_RED))

                    # ask the user to pick a brief file
                    brief_index = typer.prompt("\nWhich brief file would you like to use?", type=int)
                    brief_file, brief_file_path = brief_files[brief_index - 1]

                    # make sure brief_file_path is not None
                    if brief_file_path:
                        return brief_file_path
                    else:
                        print("Brief file path is None")
                        # exit the program
                        raise typer.Exit()
                else:
                    print("[bold red]No brief files found[/bold red] :cry:")
                    typer.confirm(
                        typer.style("Please add a brief file to the app directory and confirm", fg=typer.colors.RED), )
                    return None

            brief_file_path = check_for_briefs()
            # ask the user if they want to generate a better brief
            # print("Great briefs include :flexed_biceps: \n- database design ideas \n- functionality \n- purpose "
            #       "of the application")
            print("\n:flexed_biceps: [bold blue]Great briefs include[/bold blue] \n- database design ideas \n- "
                  "functionality \n- purpose of the application")
            generate_better_brief = typer.confirm(
                typer.style(f"Generate a better brief? (DOES NOT OVERWRITE EXISTING BREIF)",
                            bg=typer.colors.RED))

            # check if the brief file has atleast 1 line
            with open(brief_file_path, "r") as f:
                lines = f.readlines()
                if len(lines) == 0:
                    # typer.echo(typer.style("Brief file is empty", fg=typer.colors.RED))
                    # print("Brief file is empty :cry:")
                    print("[bold red]Brief file is empty[/bold red] :cry:")
                    raise typer.Exit()

            with open(brief_file_path, "r") as f:
                purpose = f.read()
            django_app = DjangoApplication(app_name, purpose, appdir)
            django_app.generate(better_brief=generate_better_brief)

            print("[bold green]Congrats. Generation is complete! :tada:[/bold green]")
            print("[bold blue]Made by @fauzaanu[/bold blue]")
            print("[bold red]:red_envelope: https://t.me/fauzaanu[/bold red]")
            print("[bold green]Happy Coding! :smiley:[/bold green]")
            print(
                "[blue]'Forget about trying, because if you’re just trying, then losing is still an option'[/blue]["
                "gray] -"
                "Tim Grover[/gray]")
        else:
            # typer.echo("No Django Apps found.")
            # print("No Django Apps found. :cry:")
            print("[bold red]No Django Apps found.[/bold red] :cry:")


if __name__ == "__main__":
    typer.run(AssistedDjangoCLI)
