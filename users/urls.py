# users/urls.py
from django.urls import path
from .views import (
    FollowUserView,
    UnfollowUserView,
    UserViewSet,
    RegisterUserView,
    UserLoginView,
    UserProfileView,
    ChangePasswordView,
    UpdateProfileView,
    ResetPasswordView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls + [
    path("follow/<int:user_id>/", FollowUserView.as_view()),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view()),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user_login'),

    # User profile view and update
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),

    # Password endpoints
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]