
import time
from config import Priority
from typing import Dict

class Notification:
    def __init__(self, message_template: str, priority: Priority, channel: str,
                 recipient: str, template_data: Dict = None):
        self.message_template = message_template
        self.priority = priority
        self.channel = channel
        self.recipient = recipient
        self.template_data = template_data or {}
        self.timestamp = time.time()
        self.retry_count = 0

    @property
    def constructed_message(self):
        return self.message_template.format(**self.template_data)

    def __repr__(self):
        return f"""[{self.priority.name}] {self.constructed_message}
                    to {self.recipient}"""
