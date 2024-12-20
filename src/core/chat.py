from src.core.flow import Flow
from enum import Enum
import utils.system_messages as system_messages

class Role(Enum):
    USER = 1
    ASSISTANT = 2


class Chat:

    def __init__(self):
        self.messages = []
        self.flow = Flow()

    def get_user_text(self):
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit', 'q']:
                system_messages.exiting_luminary()
        except (EOFError, KeyboardInterrupt):
            system_messages.exiting_luminary()
        return user_input

    def add_step(self, role: Role, content: str):
        """
        Add a message step to the chat history.

        Args:
            role (Role): The role of the message sender (USER or ASSISTANT)
            content (str): The content of the message
        """
        message = {
            "role": role.name.lower(),
            "content": content
        }
        self.messages.append(message)
    
    def stream(self, response):
        print("assistant: ", response)
        return response


    def chitchat(self):
        while True:
            self.add_step(role=Role.USER, content=self.get_user_text())
            self.add_step(role=Role.ASSISTANT, content=self.stream(response=self.flow.infer(self.messages)))
