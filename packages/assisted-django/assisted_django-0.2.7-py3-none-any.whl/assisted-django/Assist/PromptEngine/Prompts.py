from .BasePromptEngine import ModelBriefPromptEngine, BriefPromptEngine
from .examples import MODEL_EXAMPLE, FORMS_EXAMPLE, ADMIN_EXAMPLE, TESTS_EXAMPLE, URLS_EXAMPLE, SIGNALS_EXAMPLE, \
    VIEWS_EXAMPLE


class ModelPromptEngine(BriefPromptEngine):
    # Models.py should have access to the brief
    def __init__(self, brief):
        super().__init__(brief)
        self.file = 'models.py'
        self.example = MODEL_EXAMPLE


class FormsPromptEngine(BriefPromptEngine):
    # Forms.py should have access to the models.py
    def __init__(self, generated_models_file):
        super().__init__(generated_models_file)
        self.file = 'forms.py'
        self.example = FORMS_EXAMPLE


class ViewsPromptEngine(ModelBriefPromptEngine):
    # Views.py should have access to the brief and models.py
    def __init__(self, generated_models_file, brief, name):
        super().__init__(generated_models_file, brief)
        self.file = 'views.py'
        self.example = VIEWS_EXAMPLE
        self.template_instructions = (f"Important: Must be class based views and all templates"
                                      f"should be namespaced with the application name / filename.html. The "
                                      f"application name is {name}")
        self.additional_instructions = "based on the following models and project brief."

    def build_prompt(self, file):
        """
        This function builds the prompt for a given file.
        """
        system = self.get_system(
            file) + self.additional_instructions + "Models:" + self.generated_models_file + "Brief" + self.brief + self.template_instructions
        prompt = self.get_response_format(file, self.example)
        return system, prompt


class URLPromptEngine(ViewsPromptEngine):
    # Urls.py should have access to the views.py
    def __init__(self, generated_views_file, brief, name):
        super().__init__(generated_views_file, brief, name)
        self.file = 'urls.py'
        self.example = URLS_EXAMPLE


class AdminPromptEngine(ModelPromptEngine):
    # Admin.py should have access to the models.py
    def __init__(self, generated_models_file):
        super().__init__(generated_models_file)
        self.file = 'admin.py'
        self.example = ADMIN_EXAMPLE


class TestPromptEngine(ViewsPromptEngine):
    # Tests.py should have access to the views.py
    def __init__(self, generated_views_file, brief, name):
        super().__init__(generated_views_file, brief, name)
        self.file = 'tests.py'
        self.example = TESTS_EXAMPLE


class SignalsPromptEngine(ModelBriefPromptEngine):
    # Views.py should have access to the brief and models.py
    def __init__(self, generated_models_file, brief):
        super().__init__(generated_models_file, brief)
        self.file = 'signals.py'
        self.example = SIGNALS_EXAMPLE
