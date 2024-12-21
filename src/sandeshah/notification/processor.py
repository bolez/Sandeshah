
from typing import Dict

from sandeshah.channel.email import EmailChannel
from sandeshah.config import Priority
from sandeshah.notification.base import Notification
from sandeshah.notification.handler import NotificationHandler
from sandeshah.queue.manager import QueueManager


class NotificationProcessor:
    def __init__(self, queue_manager: QueueManager, max_retries: int = 3):
        self.queue_manager = queue_manager
        self.handlers = {
            "email": NotificationHandler(EmailChannel(), max_retries)
        }

    def add_notification(self, message_template: str, priority:
                         Priority, channel: str, recipient: str,
                         template_data: Dict = None):
        notification = Notification(
            message_template, priority, channel, recipient, template_data)
        self.queue_manager.enqueue(notification, priority)

    def process_notifications(self):
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            while not self.queue_manager.is_empty(priority):
                notification = self.queue_manager.dequeue(priority)
                handler = self.handlers.get(notification.channel)
                if handler:
                    handler.process(notification)
                else:
                    print(f"Invalid channel: {notification.channel}")

    def get_logs(self):
        logs = []
        for handler in self.handlers.values():
            logs.extend(handler.get_logs())
        return logs
