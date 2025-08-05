from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User, Message, Conversation
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    A view set for managing User instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A view set for managing conversation instances.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewse for viewing and editing message instances.

    Attributes:
        serilizer_class (MessageSerilizer): The serilizer class used for
            validating deserilizing input, and for serilizing output
        permission_class (list): A list of permission class that determin
            whether a user has access to the view set.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation__pk=conversation_id)

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(
            pk=self.kwargs['conversation_pk'],
        )
        serializer.save(sender=self.request.user, conversation=conversation)
