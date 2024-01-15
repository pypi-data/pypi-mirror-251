import os

from dotenv import load_dotenv
from openai import OpenAI


class OpenAISettings:
    def __init__(self):
        load_dotenv()
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
