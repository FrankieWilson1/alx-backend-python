from django.contrib import admin
from .models import Message, MessageHistory, User


admin.site.register(User)
admin.site.register(Message)
admin.site.register(MessageHistory)
