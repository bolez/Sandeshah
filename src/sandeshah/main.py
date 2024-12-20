from config import Priority
from notification.processor import NotificationProcessor
from queue.inmemory import InMemoryQueueManager

queue_manager = InMemoryQueueManager()
processor = NotificationProcessor(queue_manager, max_retries=2)

# Add Notifications
processor.add_notification(
    message_template="Hello {name}, your order #{order_id} has been shipped!",
    priority=Priority.HIGH,
    channel="email",
    recipient="gbole@example.com",
    template_data={"name": "gbole", "order_id": 12345},
)
processor.add_notification(
    message_template="Login detected from {location}. Reset your password if not you.",
    priority=Priority.MEDIUM,
    channel="email",
    recipient="dbole@example.com",
    template_data={"location": "Mumbai"},
)
processor.add_notification(
    message_template="Payment failed for order #{order_id}. Please retry.",
    priority=Priority.HIGH,
    channel="email",
    recipient="9876543210",
    template_data={"order_id": 9876},
)

# Process Notifications
print("\nProcessing notifications...")
processor.process_notifications()

# Display Logs
print("\nLogs:")
for log in processor.get_logs():
    print(log)
