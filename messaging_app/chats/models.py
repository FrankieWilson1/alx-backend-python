from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(
				'Superuser must be assigned to is_staff=True.'
			)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
				'Superuser must be assigned to is_superuser=True.'
			)
        return self.create_user(email, password, **extra_fields)

# -- User Models ---
class User(AbstractUser):
    """
    A custom User model extending AbstractUser to add additional fields.
    """
    class RoleChoices(models.TextChoices):
        GUEST = 'guest', _('Guest')
        HOST = 'host', _('Host')
        ADMIN = 'admin', _('Admin')

    first_name = models.CharField(_("first name"), max_length=150,
                                  blank=False, null=False)
    last_name = models.CharField(_("last name"), max_length=150,
                                 blank=False, null=False)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    email = models.EmailField(_("email address"), unique=True)
    # password_hash is added to match the project's explicit requiremt.
    password_hash = models.CharField(max_length=128, null=False, blank=False, default='placeholder_hash')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.GUEST,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()
    #   'email' to be used as a unique identifieer for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'role']

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """
    Model to track conversation between users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        editable=False)
    participants_id = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the conversation class to the admin
        """
        return f"Conversation {self.conversation_id}"

    class Meta:
        ordering = ['created_at']


class Message(models.Model):
    """
    Model for individual messages within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)
    sender_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(
        'conversation',
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def __str__(self):
        """String representation of the message class to the admin
        """
        sender_email = self.sender.id
        conv_id = self.conversation.conversation_id
        full_message_body = self.message_body
        if len(full_message_body) > 50:
            return (f"Msg from {sender_email} in {conv_id}: "
                    f"{full_message_body[:47]}...")
        else:
            return f"Msg from {sender_email} in {conv_id}: {full_message_body}"

    class Meta:
        ordering = ['sent_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(
				'Superuser must be assigned to is_staff=True.'
			)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
				'Superuser must be assigned to is_superuser=True.'
			)
        return self.create_user(email, password, **extra_fields)
