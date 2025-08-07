from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """
    message = "You are not a participant of this conversation."
    
    def has_permission(self, request, view):
        # Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Conversation):
                return obj.participants.filter(
                    user_id=request.user.user_id
                    ).exists()
            elif isinstance(obj, Message):
                return obj.conversation.participants.filter(
                    user_id=request.user.user_id
                    ).exists()

        return obj.sender == request.user
