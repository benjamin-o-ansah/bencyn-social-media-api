# users/urls.py
from django.urls import path
from .views import FollowUserView, UnfollowUserView, UserViewSet,RegisterUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls + [
    path("follow/<int:user_id>/", FollowUserView.as_view()),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view()),
    path('register/', RegisterUserView.as_view(), name='register'),
]