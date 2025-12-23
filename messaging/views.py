from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import MessageSerializer,ConversationSerializer
# Create your views here.



class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs['conversation_id'],
            conversation__participants=self.request.user
        )


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(
            id=self.request.data.get('conversation_id'),
            participants=self.request.user
        )
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        )