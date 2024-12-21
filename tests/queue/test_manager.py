from unittest.mock import Mock

import pytest

from sandeshah.config import Priority
from sandeshah.notification.base import Notification
from sandeshah.queue.manager import QueueManager


class TestQueueManager:
    @pytest.fixture
    def queue_manager(self):
        return QueueManager()

    def test_enqueue_not_implemented(self, queue_manager):
        notification = Mock(spec=Notification)
        priority = Mock(spec=Priority)
        with pytest.raises(NotImplementedError):
            queue_manager.enqueue(notification, priority)

    def test_dequeue_not_implemented(self, queue_manager):
        priority = Mock(spec=Priority)
        with pytest.raises(NotImplementedError):
            queue_manager.dequeue(priority)

    def test_is_empty_not_implemented(self, queue_manager):
        priority = Mock(spec=Priority)
        with pytest.raises(NotImplementedError):
            queue_manager.is_empty(priority)