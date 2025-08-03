import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    sent_at_start = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_at_end = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    
    class Meta:
        model = Message
        fields = ['sender_id', 'sent_at_start', 'sent_at_end']
