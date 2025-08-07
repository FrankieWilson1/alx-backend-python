from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'personal info',
            {'fields': ('first_name', 'last_name', 'phone_number', 'role')}
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions'
                )
            }
        ),
        (
            'Important dates',
            {
                'fields': ('last_login', 'date_joined')
            }
        ),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    filter_horizontal = ('participants', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'message_body', 'sent_at')
    list_filter = ('conversation', )
    search_fields = ('sender__first_name', 'message_body')
