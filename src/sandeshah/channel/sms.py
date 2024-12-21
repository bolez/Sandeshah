from sandeshah.channel import Channel
from sandeshah.notification.base import Notification

class SMSChannel(Channel):
    def send(self, notification: Notification):
        print(f"SMS sent to {notification.recipient}: {notification.constructed_message}")
