import django_filters

from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Allows filter messages by the sender and within a date range using
    sent_at
    """
    sent_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['sender', 'sent_at']
