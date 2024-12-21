from sandeshah.config import Priority
from sandeshah.notification.base import Notification
from sandeshah.queue.manager import QueueManager


class InMemoryQueueManager(QueueManager):
    def __init__(self):
        self.queues = {
            Priority.HIGH: [],
            Priority.MEDIUM: [],
            Priority.LOW: [],
        }

    def enqueue(self, notification: Notification, priority: Priority):
        self.queues[priority].append(notification)
        print(f"Enqueued: {notification}")

    def dequeue(self, priority: Priority):
        if self.queues[priority]:
            return self.queues[priority].pop(0)

    def is_empty(self, priority: Priority) -> bool:
        return len(self.queues[priority]) == 0
