from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings


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
    content = models.TextField(null=False)
    edited = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

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
