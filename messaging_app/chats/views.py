from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .permissions import IsParticipantOfConversation
from .models import User, Message, Conversation
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
    UserRegisterSerializer,
)
from .filters import MessageFilter


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
    permission_classes = [IsParticipantOfConversation]

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
    permission_classes = [IsParticipantOfConversation]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_pk']
        user = self.request.user

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation does not exist.")

        if not conversation.participants.filter(
            user_id=user.user_id
        ).exists():
            raise PermissionDenied(
                "You are not a participant in this conversation."
            )

        return Message.objects.filter(conversation__pk=conversation_id)

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(
            pk=self.kwargs['conversation_pk'],
        )
        serializer.save(sender=self.request.user, conversation=conversation)


class UserRegistrationView(generics.CreateAPIView):
    """
    A view set for registering new users.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = ()  # Override default `isAuthenticated` permission
    #                           and allows any user to access this endpoint
