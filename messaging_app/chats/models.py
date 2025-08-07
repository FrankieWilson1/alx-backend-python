from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """
    A user model

    Attributes:
        user_id (UUID): The unique identifier for the user.
        first_name (str): The user's given name.
        last_name (str): The user's family name.
        phone_number (str): The user's contact phone number
        role (str): The user's role in the application (e.g., 'guest', 'admin')
        created_at (DateTime): The timestamp of when a user is created.
        groups (ManyToMany): The group this user belongs to
        user_permissions (ManyToMany): Specific permissions granted to this
                                      user.
    """
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    phone_number = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=50, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='chats_user_set',
        blank=True,
        help_text='The groups this user belongs to. \
            A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chats_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Conversation(models.Model):
    """
    A conversation model

    Attributes:
        conversation_id (UUID): Unique identifier for conversation
        participants (ManyToMany): A many-to-many relationship with the User
                                    model
        created_at (DateTime): The timestamp when the conversation was created.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    A message model

    Attributes:
        message_id (UUID): Unique identifier for message
        sender (ForeignKey): A foreign key to user model
        conversation (ForeignKey): A foreign key to conversation model
        message_body (Text): A text field for messages
        sent_at (DateTime): The timestamp when the message was created.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at}"
