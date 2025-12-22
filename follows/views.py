# follows/views.py
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from .models import Follow
from .serializers import FollowSerializer, UserFollowStatsSerializer
from django.contrib.auth.models import User

class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if follower == following:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(follower=follower, following=following).exists():
            return Response({"detail": "Already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=follower, following=following)
        return Response({"detail": f"You are now following {following.username}."}, status=status.HTTP_201_CREATED)

class UnfollowUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # def get_object(self):
    #     follower = self.request.user
    #     following_id = self.kwargs['user_id']
    #     try:
    #         return Follow.objects.get(follower=follower, following__id=following_id)
    #     except Follow.DoesNotExist:
    #         return None

    # def delete(self, *args, **kwargs):
    #     follower = self.request.user
    #     try:
    #         following = self.kwargs['user_id']
    #     except User.DoesNotExist:
    #         return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    #     follow_instance = Follow.objects.filter(follower=follower, following=following).first()
    #     if not follow_instance:
    #         return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

    #     follow_instance.delete()
    #     return Response({"detail": f"You have unfollowed {following.username}."}, status=status.HTTP_204_NO_CONTENT)
    def delete(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        follow_instance = Follow.objects.filter(follower=follower, following=following).first()
        if not follow_instance:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({"detail": f"You have unfollowed {following.username}."}, status=status.HTTP_204_NO_CONTENT)

class UserFollowStatsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowStatsSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'