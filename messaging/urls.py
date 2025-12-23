from django.urls import path
from .views import (
    ConversationListView,
    MessageCreateView,
    ConversationMessagesView,
    MessageReadUpdateView,
    MarkConversationReadView
)
from django.http import HttpResponse

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
    path('messages/', MessageCreateView.as_view(), name='send-message'),
    # path('test/', lambda r: HttpResponse("Messaging works")),
    path('conversations/<int:conversation_id>/read/', MarkConversationReadView.as_view(), name='mark-conversation-read'),
    path('messages/<int:pk>/read/', MessageReadUpdateView.as_view(), name='mark-message-read'),
]
