# follows/urls.py
from django.urls import path
from .views import FollowUserView, UnfollowUserView,UserFollowStatsView

urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view()),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view()),
    path('users/<int:id>/stats/', UserFollowStatsView.as_view(), name='user-stats'),
]