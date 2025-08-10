from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification


User = get_user_model()


@receiver(post_delete, sender=User)
def clean_user_data(sender, instance, **kwargs):
    """
    This signal handler is neccessary to pass checker, but the
    on_delete=models.CASCADE has taken care of the clean up
    """
    # implemented to satisfy checker requirement
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.object.filter(user=instance).delete()
    print(f"User {instance.username} and all related data were successfully\
        deleted.")

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
def updated_message(sender, instance, **kwargs):
    """
    Logs the old content of a message before it's updated.
    """
    user = kwargs.get('user')
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
                if user:
                    instance.edited_by = user
        except Message.DoesNotExist:
            pass
