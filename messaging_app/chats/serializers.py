from rest_framework import serializers

from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """A user serializer modeling a user and it's field"""
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'username',
            'role',
            'email',
            'created_at',
            'phone_number'
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    """A user serializer modeling a user and it's field"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class MessageSerializer(serializers.ModelSerializer):
    """
    A message serializer modeling Message model
    Attribute:
        sender (Userserializer): The Userserializer class
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sent_at',
            'message_body'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """
    A Conversation serializer modeling conversation model

    Attributes:
        participants (Userserializer): The User serializer class
        message_set (Messageserializer): The message serializer class
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

    def create(self, validate_data):
        participants_data = self.context['request'].data.get('participants')
        conversation = Conversation.objects.create()
        for user_id in participants_data:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
        return conversation
