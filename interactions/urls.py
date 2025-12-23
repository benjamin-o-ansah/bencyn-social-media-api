from django.urls import path
from .views import LikePostView, CommentCreateListView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostView.as_view()),
    path('posts/<int:post_id>/comments/', CommentCreateListView.as_view()),
]
