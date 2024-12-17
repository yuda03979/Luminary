from .ollama_api import OllamaApi


def tool_func(var1: str, var2: int):
    return var1, var2


get_file_tool = {
    'type': 'function',
    'function': {
        'name': 'tool_func',
        'description': 'FILL HERE THE FUNC DESCRIPTION',
        'parameters': {
            'type': 'object',
            'required': ['var1', 'var2'],
            'properties': {
                'var1': {'type': 'string', 'description': 'VAR1 DESCRIPTION'},
                'var2': {'type': 'integer', 'description': 'VAR2 DESCRIPTION'},
            }
        }
    }
}


class OllamaToolsApi(OllamaApi):

    def __init__(self, model_name):
        super().__init__(model_name)

    # need to feel
