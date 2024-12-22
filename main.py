import sys
from pathlib import Path

# Add the `src` directory to `sys.path`
sys.path.append(str(Path(__file__).resolve().parent / "src"))

from sandeshah.config import Priority
from sandeshah.notification.processor import NotificationProcessor
from sandeshah.queue.inmemory import InMemoryQueueManager
from sandeshah.queue.sqs import SQSQueueManager

queue_manager = SQSQueueManager()
processor = NotificationProcessor(queue_manager, max_retries=2)

# Add Notifications
processor.add_notification(
    message_template="Hello {name}, yours order #{order_id} has been shipped!",
    priority=Priority.HIGH,
    channel="email",
    recipient="gbole@example.com",
    template_data={"name": "gbole", "order_id": 12345},
)
processor.add_notification(
    message_template="Login detected from {location}. Reset your password if not you.",
    priority=Priority.HIGH,
    channel="email",
    recipient="dbole@example.com",
    template_data={"location": "Mumbai"},
)
processor.add_notification(
    message_template="Payment failed for order1 #{order_id}. Please retry.",
    priority=Priority.HIGH,
    channel="email",
    recipient="9876543210",
    template_data={"order_id": 9876},
)
import time
time.sleep(30)
# Process Notifications
print("\nProcessing notifications...")
processor.process_notifications()

# Display Logs
print("\nLogs:")
for log in processor.get_logs():
    print(log)
