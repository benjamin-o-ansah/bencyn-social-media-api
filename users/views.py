# users/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,viewsets, permissions
from django.contrib.auth.models import User
from .models import Follow
from .serializers import UserSerializer

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user_to_follow == request.user:
            return Response(
                {"error": "You cannot follow yourself"},
                status = 400
            )

        Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )
        return Response({"message": "User followed"}, status=201)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        Follow.objects.filter(
            follower=request.user,
            following_id=user_id
        ).delete()

        return Response({"message": "User unfollowed"}, status=200)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
