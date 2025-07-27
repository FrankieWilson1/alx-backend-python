from rest_framework import serializers
from .models import User, Conversation, Message    # My chat user model
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    """
    A class that defines a serializer (that is directly
    tied to a Django model)
    """
    email = serializers.CharField(max_length=255)


    class Meta:
        """
        Inner class that provides options for the outer class
        """
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'created_at', 'password')
        # 'password' field is made write-only for security and required
        # for user creation
        extra_kwargs = {
			'password': {'write_only': True, 'required': True}
		}

    def create(self, validated_data):
        """Overides create to correctly andl password hasing for AbstractUser"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Overides create to correctly handle password hashing for AbstractUser"""
        password = validated_data.pop('password', None)	 # Password might not be provided on update
        if password is not None:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message Model, with nested sender details
    """
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'conversation',
                  'message_body', 'sent_at', 'updated_at')
        read_only_fields = ('message_id', 'sender', 'sent_at', 'updated_at')
    
    def validate_message_body(self, value):
        """
        Custom validation to check that the message body is not empty.
        """
        if not value.strip():	# .strip() removes leading/trailing whitespace
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation Model.
    """
    # Uses PrimaryKeyRelatedField for participants during creation/update
    # (write_only)
    participants_id = serializers.PrimaryKeyRelatedField(
		queryset=User.objects.all(), many=True, write_only=True, required=False
	)
    # Nested representation of participants for read operations(read_only)
    participants_details = UserSerializer(many=True, source='participants_id', read_only=True)

    # Add SerializedMethodField for messages to satisfy checker requirment
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('conversation_id', 'participants_id', 'created_at',
                  'participants_details', 'updated_at', 'messages', 'topic'
                  )
        read_only_fields = ('conversation_id', 'created_at', 'updated_at')
    
    def get_messages(self, obj):
        """
        Method to get and serialize messages related to this conversation.
        It retrieves all messages for the conversation and serializes them.
        """
        message_queryset = obj.messages.all().order_by('sent_at')
        return MessageSerializer(message_queryset, many=True, read_only=True).data
    
    def create(self, validated_data):
        """
        Overides create to handle ManyToManyField for participants_id
        """
        participants_data = validated_data.pop('participants_id', [])
        
        request_user = self.context.get('request').user if 'request' in self.context else None
        
        if request_user and request_user not in participants_data:
            participants_data.append(request_user)
        
        with transaction.atomic():	# Ensures database operations are atomic
            conversation = Conversation.objects.create(**validated_data)
            conversation.participants_id.set(participants_data)
        return conversation
    
    def update(self, instance, validated_data):
        """Overides update to handle ManyToManyField for participants_id"""
        participants_data = validated_data.pop('participants_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if participants_data is not None:
            request_user = self.context.get('request').user if 'request' in self.context else None
            if request_user and request_user not in participants_data:
               participants_data.append(request_user)
            instance.participants_id.set(participants_data)
        instance.save()
        return instance
