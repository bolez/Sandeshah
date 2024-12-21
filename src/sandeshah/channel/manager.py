from sandeshah.notification.base import Notification


class Channel:
    def send(self, notification: Notification):
        raise NotImplementedError
