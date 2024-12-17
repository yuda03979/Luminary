from typing import Union, Sequence
import ollama


class OllamaApi:

    def __init__(self, model_name):
        self.model_name = model_name


    def chat_stream(self, messages: list):
        response = ''
        for part in ollama.chat(self.model_name, messages=messages, stream=True):
            response += part['message']['content']
            print(part['message']['content'], end='', flush=True)
        return response


    def embed(self, input: Union[str, Sequence[str]]):
        return ollama.embed(model=self.model_name, input=input)


    def generate_schema(self):
        pass

    def get_tasks(self):
        return {
            "chat_stream": self.chat_stream,
            "embed": self.embed
        }
    
    def close(self):
        ollama.generate(model=self.model_name, keep_alive=0)
        return f"<closed model {self.model_name}>"