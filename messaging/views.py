from django.shortcuts import render
from rest_framework import generics, permissions,exceptions,response,status
from .models import Conversation, Message
from .serializers import MessageSerializer,ConversationSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.views import APIView

# Create your views here.


User = get_user_model()
class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Message.objects.filter(
    #         conversation_id=self.kwargs['conversation_id'],
    #         conversation__participants=self.request.user
    #     )
    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]

        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).select_related("sender")

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     conversation = Conversation.objects.get(
    #         id=self.request.data.get('conversation'),
    #         participants=self.request.user
    #     )
    #     serializer.save(
    #         sender=self.request.user,
    #         conversation=conversation
    #     )
    def perform_create(self, serializer):
        # conversation = Conversation.objects.get(
        #     id=self.request.data.get("conversation")
        # )
        # conversation = serializer.validated_data['conversation']

        # if not conversation.participants.filter(id=self.request.user.id).exists():
        #     raise exceptions.PermissionDenied("You are not a participant in this conversation.")

        # serializer.save(sender=self.request.user)
        recipient_id = self.request.data.get("recipient_id")
        conversation_id = self.request.data.get("conversation")
        sender = self.request.user

        if conversation_id:
            # Case A: Replying to an existing conversation
            try:
                conversation = Conversation.objects.get(
                    id=conversation_id, 
                    participants=sender
                )
            except Conversation.DoesNotExist:
                raise exceptions.ValidationError("Conversation not found or you are not a participant.")
        else:
            # Case B: WhatsApp-style (Starting a chat via recipient_id)
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                raise exceptions.ValidationError("Recipient user does not exist.")

            if recipient == sender:
                raise exceptions.ValidationError("You cannot start a conversation with yourself.")

            # Find a conversation that has BOTH users as participants
            conversation = Conversation.objects.filter(participants=sender)\
                                               .filter(participants=recipient).first()

            # If no conversation exists between these two, create it
            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(sender, recipient)

        # Save the message
        serializer.save(sender=sender, conversation=conversation)
class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        )

class MessageReadUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure only the recipient can mark a message as read
        instance = self.get_object()
        if instance.sender == self.request.user:
            raise PermissionError("You cannot mark your own message as read.")
        serializer.save(is_read=True)

class MarkConversationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        # Update all messages in this conversation where:
        # 1. The user is NOT the sender (they are the receiver)
        # 2. The message is currently unread
        updated_count = Message.objects.filter(
            conversation_id=conversation_id,
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        return response.Response(
            {"message": f"{updated_count} messages marked as read."},
            status=status.HTTP_200_OK
        )