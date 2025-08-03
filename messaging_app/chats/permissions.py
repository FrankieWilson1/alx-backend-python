from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participantsof a conversation
    to view and interact with it.
    """
    def has_permission(self, request, view):
        # Allow access only to authenticated users.
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow access only to participants in a conversation
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.participants_id.all()

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants_id.all()
        return False
