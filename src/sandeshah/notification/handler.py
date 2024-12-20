from channel.manager import Channel
from notification.base import Notification


class NotificationHandler:
    def __init__(self, channel: Channel, max_retries: int):
        self.channel = channel
        self.max_retries = max_retries
        self.logs = []

    def process(self, notification: Notification):
        try:
            self.channel.send(notification)
            self.log(notification, "SUCCESS")
        except Exception as e:
            print(f"Error sending notification: {e}")
            self.retry(notification)

    def retry(self, notification: Notification):
        if notification.retry_count < self.max_retries:
            notification.retry_count += 1
            print(f"Retrying notification: {notification}")
            self.process(notification)
        else:
            self.log(notification, "FAILED")
            print(f"Notification failed after max retries: {notification}")

    def log(self, notification: Notification, status: str):
        log_entry = {
            "message": notification.constructed_message,
            "priority": notification.priority.name,
            "channel": notification.channel,
            "recipient": notification.recipient,
            "timestamp": notification.timestamp,
            "status": status,
            "retries": notification.retry_count,
        }
        self.logs.append(log_entry)

    def get_logs(self):
        return self.logs
