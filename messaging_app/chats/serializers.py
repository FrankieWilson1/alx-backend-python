from rest_framework import serializers
from .models import User, Conversation, Message    # My chat user model


class UserSerializer(serializers.ModelSerializer):
    """
    A class that defines a serializer (that is directly
    tied to a Django model)
    """
    class Meta:
        """
        Inner class that provides options for the outer class
        """
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'created_at')
        read_only_fields = ('user_id', 'created_at',)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation Model.
    """
    # Define a field for participants_id using the UserSerializer for nesting
    # Since participants_id is a ManyToManyField, it will be a list of User
    # objects
    participants_id = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('conversations_id', 'participants_id', 'created_at')
        read_only_fields = ('conversations_id', 'created_at',)


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message Model, with nested sender details
    """
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'conversation',
                  'message_body', 'sent_at')
        read_only_fields = ('message_id', 'sender', 'sent_at')
