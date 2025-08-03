# from django.shortcuts import render
from rest_framework import viewsets, viewsets, serializers
from .models import Conversation, User, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.core.exceptions import PermissionDenied


class ConversationViewSet(viewsets.ModelViewSet):
    """ A ViewSet for viewing and editing conversation instances"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = (IsAuthenticated, IsParticipantOfConversation,)

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
    # queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsParticipantOfConversation,)
    
    def get_queryset(self):
        """
        Filters the messages to only show those belonging to a conversation
        that the authenticated user is a participant in.
        """
        user_conversations = self.request.user.conversations.all()
        queryset = Message.objects.filter(conversation__in=user_conversations)
        return queryset

    def perform_create(self, serializer):
        """
        Overrides the default perform_create to set the sender
        (requesting user) and the conversation for a new message.
        """
        conversation_id = self.request.data.get('conversation')

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

        if self.request.user not in conversation.participants_id.all():
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
