from ollama_dir.ollama_api import OllamaApi


class Models:

    def __init__(self):
        self.models = {}
    

    def add(self, model_name):
        self.models[model_name] = OllamaApi(model_name=model_name)

    def infer(self, model_name, task, param):
        return self.models[model_name].get_tasks()[task](param)


MODELS = Models()