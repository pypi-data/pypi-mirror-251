import os

from dotenv import load_dotenv
from openai import OpenAI


class OpenAISettings:
    def __init__(self):
        # find the .env file from the current directory or the parent directory
        # this is required for the openai api key
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
        if not os.getenv("OPENAI_API_KEY"):
            load_dotenv(dotenv_path=os.path.join(os.getcwd(), '..', '.env'))
        # else:
        # # print("found from current directory")
        if not os.getenv("OPENAI_API_KEY"):
            print("Please set OPENAI_API_KEY in your .env file")
            raise SystemExit()
        # else:
        # # print("found from parent directory")

        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = 'gpt-3.5-turbo'
        self.temperature = 0.1
        self.max_tokens = 2000

    def prompt(self, system, prompt):
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
