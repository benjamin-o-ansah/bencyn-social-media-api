from django.urls import path
from .views import (
    ConversationListView,
    MessageCreateView,
    ConversationMessagesView,
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
    path('messages/', MessageCreateView.as_view(), name='send-message'),
]
