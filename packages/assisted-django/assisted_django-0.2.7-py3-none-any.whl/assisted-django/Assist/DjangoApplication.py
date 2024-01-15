import os
import random

import rich
import typer

from .openAISettings.Prompter import OpenAISettings
from .PromptEngine.Prompts import ModelPromptEngine, FormsPromptEngine, ViewsPromptEngine, URLPromptEngine, \
    AdminPromptEngine, TestPromptEngine, SignalsPromptEngine


class DjangoApplication:
    """
    This class represents a Django application.
    """

    def __init__(self, name, purpose, directory, nolog=True):
        self.name = name
        self.purpose = purpose
        self.directory = directory

    def clean_file(self, file_content):
        clean_string = [
            "```python",
            "```",
        ]
        for string in clean_string:
            if string in file_content:
                typer.echo(f"Removing {string} from file")
                file_content = file_content.replace(string, "")

        return file_content

    def generate(self, better_brief=False):
        """
        This function generates the content for the Django application.

        :param cycles: Number of cycles to run the improve_file method.
        :type cycles: int
        :return: None
        :rtype: None
        """
        # openai client
        oai_client = OpenAISettings()

        if better_brief:
            # improve the brief
            system = (f"You are tasked with expanding and detailing on the django project brief for an application. "
                      f"The general ideas for the brief are as follows: \n\n {self.purpose}")
            prompt = (f"Expand on the brief for the django application. Include details such as the purpose of "
                      f"the application, the base level functionality, and the database design")

            self.purpose = oai_client.prompt(system, prompt)

            random_number = random.randint(0, 1000)
            # ensure file does not exist
            while os.path.exists(os.path.join(self.directory, f'better_brief_{random_number}.md')):
                random_number = random.randint(0, 1000)

            with open(os.path.join(self.directory, f'better_brief_{random_number}.md'), 'w') as f:
                f.write(self.purpose)
                # logging.info("brief Updated!")
                # typer.echo("brief Updated!")
                rich.print(f"[bold green]:heavy_check_mark: brief Updated![/bold green]")

        # 1. Create the models for the project brief
        # logging.info("Creating models.py")
        # typer.echo("🤖 Creating models.py")
        rich.print(f":snake: Creating models.py")
        models_prompt = ModelPromptEngine(self.purpose)
        system, prompt = models_prompt.get_prompt()
        models_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'models.py'), 'w') as f:
            models_file_content = self.clean_file(models_file_content)
            f.write(models_file_content)
            # logging.info("models.py Updated!")
            # typer.echo("✅ models.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: models.py Updated![/bold green]")

        # 2. Create the forms for the models
        # typer.echo("🤖 Creating forms.py")
        rich.print(f":snake: Creating forms.py")
        forms_prompt = FormsPromptEngine(models_file_content)
        system, prompt = forms_prompt.get_prompt()
        forms_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'forms.py'), 'w') as f:
            f.write(forms_file_content)
            # typer.echo("✅ forms.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: forms.py Updated![/bold green]")

        # 3. Create the views for the forms
        # typer.echo("🤖 Creating views.py")
        rich.print(f":snake: Creating views.py")
        views_prompt = ViewsPromptEngine(models_file_content, self.purpose, self.name)
        system, prompt = views_prompt.get_prompt()
        views_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'views.py'), 'w') as f:
            views_file_content = self.clean_file(views_file_content)
            f.write(views_file_content)
            # typer.echo("✅ views.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: views.py Updated![/bold green]")

        # 4. Create the urls for the views
        typer.echo("🤖 Creating urls.py")
        urls_prompt = URLPromptEngine(views_file_content, self.purpose, self.name)
        system, prompt = urls_prompt.get_prompt()
        urls_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'urls.py'), 'w') as f:
            urls_file_content = self.clean_file(urls_file_content)
            f.write(urls_file_content)
            # typer.echo("✅ urls.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: urls.py Updated![/bold green]")

        # 5. Create the admin for the models
        # typer.echo("🤖 Creating admin.py")
        rich.print(f":snake: Creating admin.py")
        admin_prompt = AdminPromptEngine(models_file_content)
        system, prompt = admin_prompt.get_prompt()
        admin_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'admin.py'), 'w') as f:
            admin_file_content = self.clean_file(admin_file_content)
            f.write(admin_file_content)
            # typer.echo("✅ admin.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: admin.py Updated![/bold green]")

        # 6. Create the tests for the views
        typer.echo("🤖 Creating tests.py")
        tests_prompt = TestPromptEngine(views_file_content, self.purpose, self.name)
        system, prompt = tests_prompt.get_prompt()
        tests_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'tests.py'), 'w') as f:
            tests_file_content = self.clean_file(tests_file_content)
            f.write(tests_file_content)
            # typer.echo("✅ tests.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: tests.py Updated![/bold green]")

        # 7. Create the signals for the models
        # typer.echo("🤖 Creating signals.py")
        rich.print(f":snake: Creating signals.py")
        signals_prompt = SignalsPromptEngine(models_file_content, self.purpose)
        system, prompt = signals_prompt.get_prompt()
        signals_file_content = oai_client.prompt(system, prompt)
        with open(os.path.join(self.directory, 'signals.py'), 'w') as f:
            signals_file_content = self.clean_file(signals_file_content)
            f.write(signals_file_content)
            # typer.echo("✅ signals.py Updated!")
            rich.print(f"[bold green]:heavy_check_mark: signals.py Updated![/bold green]")

        # 8. Create the templates for the views
        # typer.echo("🤖 Creating templates")
        rich.print(f":snake: Creating templates")
        templates_directory = os.path.join(self.directory, 'templates')
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)

        # namespace directory with app name
        templates_directory = os.path.join(templates_directory, self.name)
        if not os.path.exists(templates_directory):
            os.makedirs(templates_directory)

        # find the mention of the template directory in the views.py file
        # 'self.name/*.html'

        # find all the template names in the views.py file
        templates = []
        for line in views_file_content.split("\n"):
            if "template_name" in line:
                # additionally ensure that .html and self.name are in the line
                if ".html" in line and self.name in line:
                    import re
                    # format: /*.html or \w+\.html
                    # followed by a slash have any name and ends with .html
                    template_name = re.findall(r'\w+\.html', line)[0]
                    templates.append(template_name)

        rich.print(f":magnifying_glass_tilted_left: Found the following templates: {templates}")
        # create the templates
        for template in templates:
            template_file = os.path.join(templates_directory, template)
            # call openai directly
            system = (f"You are tasked with creating the {template} template for the {self.name} application. The "
                      f"following are additional details that maybe relevant to the template creation:")
            system += "\n\n Models: \n\n" + models_file_content
            system += "\n\n Views: \n\n" + views_file_content
            system += "\n\n Urls: \n\n" + urls_file_content
            prompt = (f"Create a responsive and accessible HTML markup for {template} template using Bootstrap. "
                      f"Utilize Bootstrap's grid system, components, and utility classes for efficient design. Ensure "
                      f"semantic structure with HTML tags, incorporate ARIA for accessibility, and validate markup "
                      f"for standards compliance.")
            answer = oai_client.prompt(system, prompt)
            with open(template_file, 'w') as f:
                f.write(answer)
                # logging.info(f"{template} Updated!")
                # typer.echo(f"✅ {template} Updated!")
                rich.print(f"[bold green]:heavy_check_mark: {template} Updated![/bold green]")

        # logging.info("All Template files updated!")
        # [bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:
        # typer.echo("✅✅ All Template files updated!")
        rich.print("[bold green]:heavy_check_mark: All Template files updated![/bold green]")
