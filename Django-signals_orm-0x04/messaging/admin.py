from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Message, Notification, MessageHistory


class UserAdmin(BaseUserAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'receiver',
        'content',
        'edited_by',
        'edited'
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['edited_by'].required = False
        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.sender = request.user
        super().save_model(request, obj, form, change)

User = get_user_model()
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification)
admin.site.register(MessageHistory)
