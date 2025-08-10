from django.db import models
from django.db.models import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user: User) -> QuerySet:
        return self.filter(receiver=user, read=False)
