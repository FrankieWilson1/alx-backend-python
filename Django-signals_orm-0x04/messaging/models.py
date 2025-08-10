from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.db.models import F


class User(AbstractUser):
    """
    A user model

    Attributes:
        user_id (UUID): The unique identifier for the user.
        phone_number (str): The user's contact phone number
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    phone_number = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class MessageManager(models.Manager):
    """
    Implement a recursive query
    """
    def get_threaded_messages(self, message_id):

        root_message = self.filter(
            message_id=message_id
        ).first()

        if not root_message:
            return []

        all_messages = self.filter(
            models.Q(
                parent_message=root_message
            ) | models.Q(
                parent_message__parent_message=root_message
            )
        ).select_related(
            'sender',
            'receiver'
        ).prefetch_related(
            'replies'
        ).order_by('sent_at')

        # Combine the root message and replies into a single list
        messages = [root_message] + list(all_messages)

        # Build a nested dictionary or list to represent the thread in python
        threaded_messages = {}
        for msg in messages:
            threaded_messages[msg.message_id] = {
                'message': msg,
                'replies': []
            }

        # Build the thread by linking replies to their parents.
        for msg in messages:
            if msg.parent_message_id in threaded_messages:
                threaded_messages[msg.parent_message_id]['replies'].append(
                    threaded_messages[msg.message_id]
                )

        # Return the root of the conversation tree
        return threaded_messages.get(root_message.message_id)


class Message(models.Model):
    """
    A message model

    Attributes:
        message_id (UUID): Unique identifier for message
        sender (ForeignKey): A foreign key to user model
        content (Text): A text field for messages
        edited (Boolean): indicates if a message has been edited or not
        sent_at (DateTime): The timestamp when the message was created.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='edited_by',
        on_delete=models.CASCADE,
        null=True
    )
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='replies',
        null=True,
        blank=True
    )
    content = models.TextField(null=False)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"


class Notification(models.Model):
    """
    A class model that triggers notifications
    """
    notification_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.first_name} about message\
            {self.message.pk}"


class MessageHistory(models.Model):
    """
    A class model that stores the old content of a message before it's updated
    """
    history_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history'
        )
    old_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.pk} at {self.created_at}"
