from channel.manager import Channel
from notification.base import Notification


class EmailChannel(Channel):
    def send(self, notification: Notification):
        print(f"""
                Email sent to {notification.recipient}:
                {notification.constructed_message}"""
              )
