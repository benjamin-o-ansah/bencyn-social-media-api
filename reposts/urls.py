from django.urls import path
from .views import RepostView

urlpatterns = [
    path('posts/<int:post_id>/repost/', RepostView.as_view(), name='repost'),
]
