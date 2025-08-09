from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Creates a notification for the receiver of a new message
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def updated_message(sender, instance, **Kwargs):
    """
    Logs the old content of a message before it's updated.
    """
    # Checks if the instance already exists in the database.
    if instance.pk:
        try:
            # Get the old version of the message from the database
            old_message = Message.objects.get(pk=instance.pk)

            # Check for changes of the old message in MessageHistory
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Sets flag to tru
                instance.edited = True
        except Message.DoesNotExist:
            pass
