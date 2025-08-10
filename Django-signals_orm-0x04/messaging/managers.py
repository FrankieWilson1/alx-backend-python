from django.db import models
from django.db.models import QuerySet


class UnreadMessagesManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(read=False)

    def by_user(self, user):
        return self.get_queryset().filter(
            receiver=user
        ).onley(
            'message_id',
            'sender_id',
            'content',
            'sent_at'
        )
