from typing import Union, Sequence
import ollama


class OllamaApi:

    def __init__(self, model_name):
        self.model_name = model_name


    def chat(self, messages: list):
        return ollama.chat(self.model_name, messages=messages).message.content


    def embed(self, input: Union[str, Sequence[str]]):
        return ollama.embed(model=self.model_name, input=input)


    def generate_schema(self, schema):
        pass

    def get_tasks(self):
        return {
            "chat": self.chat,
            "embed": self.embed
        }