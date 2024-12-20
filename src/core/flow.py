from utils.models import MODELS
from utils.globals import GLOBALS



class Flow:

    def __init__(self):
        self.model_name = GLOBALS.model_name
        MODELS.add(self.model_name)


    def infer(self, messages: list[dict]):
        return MODELS.infer(model_name=self.model_name, task="chat", param=messages)