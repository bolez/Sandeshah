from typing import Any

from config import Priority
from notification.base import Notification


class QueueManager:
    def enqueue(self, notification: Notification, priority: Priority):
        raise NotImplementedError

    def dequeue(self, priority: Priority) -> Any:
        raise NotImplementedError

    def is_empty(self, priority: Priority) -> bool:
        raise NotImplementedError
