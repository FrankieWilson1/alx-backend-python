from rest_framework import serializers

from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """A user serilizer modeling a user and it's field"""
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'role',
            'email',
            'created_at',
            'phone_number'
        ]


class MessageSerializer(serializers.ModelSerializer):
    """
    A message serilizer modeling Message model
    Attribute:
        sender (UserSerilizer): The UserSerilizer class
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sent_at',
            'message_body'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """
    A Conversation serilizer modeling conversation model

    Attributes:
        participants (UserSerilizer): The User serilizer class
        message_set (MessageSerilizer): The message serilizer class
    """
    participants = UserSerializer(read_only=True, many=True)
    message_set = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = [
            'participants',
            'message_set',
            'conversation_id',
            'created_at'
        ]
