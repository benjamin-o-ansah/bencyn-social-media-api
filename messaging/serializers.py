from rest_framework import serializers
from .models import Message,Conversation


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'content',
            'created_at',
        ]
        read_only_fields = ['sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'updated_at',
        ]