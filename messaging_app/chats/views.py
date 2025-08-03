# from django.shortcuts import render
from rest_framework import viewsets, viewsets, status, serializers
from rest_framework.response import Response
from .models import Conversation, User, Message
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .permissions import IsParticipant
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


class ConversationViewSet(viewsets.ModelViewSet):
    """ A ViewSet for viewing and editing conversation instances"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = (IsParticipant, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Overrides the default perform_create to handle Many-to-many
        participants relationship for new conversation
        """
        # Saves conversation instance first without participants.
        conversation = serializer.save()

        # Accesses request.data directly for participants_id
        participant_ids = self.request.data.get('participants_id', [])

        # Adds participants to the conversation
        if participant_ids:
            # filters valid objects based on the provided IDs
            users_to_add = User.objects.filter(user_id__in=participant_ids)
            conversation.participants_id.set(users_to_add)
        
        # Adds requesting user to the conversation automatically if they are
        # not already included
        if self.request.user.is_authenticated and self.request.user not in users_to_add:
            conversation.participants_id.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """A ViewSet for viewing and sending message instaces."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """
        Overrides the default perform_create to set the sender
        (requesting user) and the conversation for a new message.
        """
        # Ensures message is linked to the authenticated user as sender
        # and to the spcified conversation.

        # Get the conversation ID from the request data
        # Assuming the client sends 'conversation' as a UUID string
        conversation_id = self.request.data.get('conversation')

        # Adds participants to the conversation
        if not conversation_id:
            # raises error
            raise serializers.ValidationError(
                {"conversation": "Conversation ID is required to send a message."}
            )
        try:
            conversation = Conversation.objects.get(conversations_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError(
                {"conversation": "Conversation with this ID does not exist."}
            )

        serializer.save(sender=self.request.user, conversation=conversation)
