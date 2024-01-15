class BasePromptEngine:
    def __init__(self):
        self.file = ""
        self.example = ""

    # Each Prompt Engine should have a basic system prompt and response format

    def get_system(self, file):
        """
        This function generates the system prompt for a given file along with the brief.
        """
        return f"You are tasked with generating the {file} Python code for a Django application"

    def get_response_format(self, file, example):
        """
        This function generates the response format for a given file.
        """
        return f"Ensure that the {file} file adheres to the following format:" + example

    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(file)
        prompt = self.get_response_format(file, self.example)
        return system, prompt

    def get_prompt(self):
        return self.build_prompt(self.file)


class ModelBriefPromptEngine(BasePromptEngine):
    # Views.py should have access to the brief and models.py
    def __init__(self, generated_models_file, brief):
        super().__init__()
        self.generated_models_file = generated_models_file
        self.brief = brief
        self.additional_instructions = "based on the following models and project brief."


    # override the base response format to add models.py as views should have access to the models.py
    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(
            file) + self.additional_instructions + "Models:" + self.generated_models_file + "Brief" + self.brief
        prompt = self.get_response_format(file,self.example)
        return system, prompt


class BriefPromptEngine(BasePromptEngine):
    # Models.py should have access to the brief
    def __init__(self, brief):
        super().__init__()
        self.brief = brief
        self.additional_instructions = "based on the following project brief."

    # override the base system prompt to add brief as models should have access to the brief
    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(file) + self.additional_instructions + "Brief:" + self.brief
        prompt = self.get_response_format(file, self.example)
        return system, prompt


class ModelPromptEngine(BriefPromptEngine):
    # Forms.py should have access to the models.py
    def __init__(self, generated_models_file):
        super().__init__()
        self.generated_models_file = generated_models_file
        self.additional_instructions = "based on the following models.py file."

    # override the base response format to add models.py as forms should have access to the models.py
    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(file) + self.additional_instructions + "Models:" + self.generated_models_file
        prompt = self.get_response_format(file,self.example)
        return system, prompt


class ViewsPromptEngine(BasePromptEngine):
    # Urls.py should have access to the views.py
    def __init__(self, generated_views_file):
        super().__init__()
        self.generated_views_file = generated_views_file
        self.additional_instructions = "based on the following views.py file."

    # override the base response format to add views.py as urls should have access to the views.py
    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(file) + self.additional_instructions + "Views:" + self.generated_views_file
        prompt = self.get_response_format(file,self.example)
        return system, prompt
