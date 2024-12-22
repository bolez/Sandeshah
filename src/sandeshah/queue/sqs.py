import boto3

from sandeshah.config import Priority
from sandeshah.notification.base import Notification
from sandeshah.queue.manager import QueueManager


class SQSQueueManager(QueueManager):

    def __init__(self):
        self.queues = {
            Priority.HIGH: "https://sqs.us-east-1.amazonaws.com/971422681393/start1",
            Priority.MEDIUM: [],
            Priority.LOW: [],
        }
        self.sqs_client = boto3.client("sqs")

    def enqueue(self, notification: Notification, priority: Priority) -> None:
        queue_url = self.queues[notification.priority]
        self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=notification.constructed_message,
            MessageAttributes={
                "Channel": {"DataType": "String",
                            "StringValue": notification.channel},
                "Recipient": {"DataType": "String",
                              "StringValue": notification.recipient},
                "Priority": {"DataType": "String",
                             "StringValue": notification.priority.name},
            },
        )
        print(f"Enqueued: {notification}")

    def dequeue(self, priority: Priority):
        queue_url = self.queues[priority]
        if not queue_url:
            return None
        response = self.sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=1,
            VisibilityTimeout=10,
            WaitTimeSeconds=5,
            MessageAttributeNames=[
                'All'
            ],

        )
        if "Messages" in response:
            message = response["Messages"][0]
            notification = Notification(
                message["Body"],
                Priority[message["MessageAttributes"]
                         ["Priority"]["StringValue"]],
                message["MessageAttributes"]["Channel"]["StringValue"],
                message["MessageAttributes"]["Recipient"]["StringValue"],
            )
            receipt_handle = message["ReceiptHandle"]
            self.sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle,
            )
            return notification

    def is_empty(self, priority: Priority) -> bool:
        queue_url = self.queues[priority]
        if not queue_url:
            return True
        response = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages',
                            'ApproximateNumberOfMessagesNotVisible',
                            'ApproximateNumberOfMessagesDelayed']
        )
        message_count = int(response['Attributes']
                            ['ApproximateNumberOfMessages'])
        return message_count == 0
