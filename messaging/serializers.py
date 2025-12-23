from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth.models import User



class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source="sender.username")
    # Make conversation optional so we can create it on the fly
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), 
        required=False, 
        allow_null=True
    )
    # Add a field to specify who you are sending to if it's a new chat
    recipient_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [
            "id", "conversation", "sender", "sender_username", 
            "recipient_id", "content", "created_at", "is_read"
        ]
        read_only_fields = ["sender", "created_at"]

    def validate(self, data):
        # Ensure we have either a conversation ID OR a recipient ID
        if not data.get('conversation') and not data.get('recipient_id'):
            raise serializers.ValidationError(
                "You must provide either a conversation ID or a recipient_id."
            )
        return data


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    unread_count = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ["id", "participants", "updated_at","unread_count"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()